#!/bin/bash


if [ $# -ne 7 ]; then
	echo "Incorrect number of arguments. Expected : "
	echo "./run_experiments <no_of_relays/files start_value> <no_of_relays/files stop_value> <increment(additive)> <block_size> <no_of_requests> <bulk_batch_size> <Full path to XPIR/ZT repos including trailing />"
fi

no_of_relays_start=$1
no_of_relays_stop=$2
increment=$3
block_size=$4
no_of_requests=$5
bulk_batch_size=$6
path_to_repos=$7
pipe=/tmp/testpipe

START_PATH=$PWD"/"
RESULTS_DIRECTORY="Results"
RESULTS_XPIR_DIRECTORY=$START_PATH$RESULTS_DIRECTORY"/XPIR"
RESULTS_XPIR_PATH=$START_PATH$RESULTS_DIRECTORY"/XPIR/"
SUBSCRIPT_FOLDER=$START_PATH"subscripts/"
CLIENTLOG_FILENAME="clientlog"
SERVERLOG_FILENAME="serverlog"
PORT_RESET_COMMAND="fuser -k 1234/tcp"

if [[ ! -p $pipe ]]; then
	mkfifo $pipe
fi

XPIR_DIRECTORY="XPIR"
XPIR_SERVER_LOCATION="/_build/apps/server/"
XPIR_SERVER_LOCATION=$path_to_repos$XPIR_DIRECTORY$XPIR_SERVER_LOCATION
XPIR_TIME_EXTRACT_TEMPFILE_LOCATION="./"
XPIR_TIME_EXTRACT_TEMPFILE="client_time"

XPIR_CLIENT_LOCATION="/_build/apps/client/"
XPIR_CLIENT_LOCATION=$path_to_repos$XPIR_DIRECTORY$XPIR_CLIENT_LOCATION
XPIR_CLIENT_COMMAND="./pir_client -c -r LWE.* -x 0 -u 4000000 -d 4000000"

if [ ! -d $RESULTS_DIRECTORY ]; then
	echo $RESULTS_DIRECTORY
	mkdir $RESULTS_DIRECTORY 
fi

if [ ! -d $RESULTS_XPIR_DIRECTORY ]; then
	echo $RESULTS_XPIR_DIRECTORY
	mkdir $RESULTS_XPIR_DIRECTORY 
fi

cd $path_to_repos
if [ -d $XPIR_DIRECTORY ]; then
	echo "Folder Found for XPIR!"
else
	echo "Error : XPIR Folder not found"
	exit
fi

PY_PARSE_CLIENTLOG="python ./extract_time_xpir_client.py "$XPIR_CLIENT_LOCATION" "$CLIENTLOG_FILENAME" "$XPIR_TIME_EXTRACT_TEMPFILE 
no_of_relays=$no_of_relays_start

cd $RESULTS_XPIR_PATH
#rm *

while [ "$no_of_relays" -le "$no_of_relays_stop" ]
	do
	echo "$no_of_relays, $no_of_relays_stop"
	$PORT_RESET_COMMAND
	sleep 1s

	XPIR_SERVER_COMMAND="./pir_server --db-generator -z -n $no_of_relays -l $block_size --no-pipeline" 
	echo $XPIR_SERVER_COMMAND
	CSV_FILE_NAME="XPIR_"$no_of_relays"_"$block_size"_"$bulk_batch_size	
	PY_PARSE_SERVERLOG="python ./extract_time_xpir_server.py "$XPIR_SERVER_LOCATION" "$SERVERLOG_FILENAME" "$XPIR_TIME_EXTRACT_TEMPFILE_LOCATION" "$XPIR_TIME_EXTRACT_TEMPFILE" "$RESULTS_XPIR_PATH" "$CSV_FILE_NAME" "$bulk_batch_size

	cd $XPIR_SERVER_LOCATION
	echo ""
	$XPIR_SERVER_COMMAND > serverlog 2>&1 &  
	kill_id=$!
	#echo "KILL_ID = "$kill_id

	#Loop client_command over no_of_requests
	counter=0 

	while [ $counter != $no_of_requests ]
		do
		cd $XPIR_CLIENT_LOCATION
		$XPIR_CLIENT_COMMAND 1>$CLIENTLOG_FILENAME 2>&1
		cd $SUBSCRIPT_FOLDER
		#Parse timings from each individual clientlog to intermediate file
		#echo $PY_PARSE_CLIENTLOG		
		$PY_PARSE_CLIENTLOG
		counter=$((counter+1))
		echo $counter
		done	

	#Do serverlog parsing using the intermediate file and generated serverlog
	#echo $PY_PARSE_SERVERLOG
	#TODO: Enable ServerLOG parse
	$PY_PARSE_SERVERLOG
	no_of_relays=$((no_of_relays+increment))
	cd $SUBSCRIPT_FOLDER
	#TODO: Enable the tempfile deletion
	rm $XPIR_TIME_EXTRACT_TEMPFILE
	done
	KILL_COMMAND="pkill -9 $kill_id"
	$KILL_COMMAND
	sleep 1s

#Now we have a list of XPIR_<N>_<blocksize> files, that can be parsed/pruned to graph.
#Invoke a python script to take these files and plot the graphs.

#File format for XPIR is <GenerateQuery_time, ExtractResult_time, Request_size, Response_size, ProcessQuery_time>
#cd
#PY_GEN_GRAPH_COMMAND="./gen_graphs $PATH_TO_RESULTS_FOLDER $no_of_relays_start $no_of_relays_stop $increment $block_size $GRAPH_NAME" 

