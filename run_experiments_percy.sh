#!/bin/bash


if [ $# -ne 7 ]; then
	echo "Incorrect number of arguments. Expected : "
	echo "./run_experiments <no_of_relays/files start_value> <no_of_relays/files stop_value> <increment by(addition)> <block_size> <no_of_requests> <bulk_batch_size> <Full path to XPIR/ZT/Percy++ repos including trailing />"
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
RESULTS_PERCY_DIRECTORY="Results/Percy"
RESULTS_ITPIR_PATH=$START_PATH"Results/Percy/"
SUBSCRIPT_FOLDER=$START_PATH"subscripts/"
CLIENTLOG_FILENAME="percyclientlog"
DATABASE_FILENAME="database"
SERVER1LOG_FILENAME="percyserver1log"
SERVER2LOG_FILENAME="percyserver2log"
SERVER3LOG_FILENAME="percyserver3log"

if [[ ! -p $pipe ]]; then
	mkfifo $pipe
fi

PERCY_DIRECTORY="percy++-1.0.0/"
PERCY_LOCATION=$path_to_repos$PERCY_DIRECTORY
PERCY_TIME_EXTRACT_TEMPFILE_LOCATION="./"
PERCY_TIME_EXTRACT_TEMPFILE="percy_time"

#PORT_RESET_COMMAND="fuser -k 1234/tcp"
#TODO : sudo -k fuser 1234/tcp
#	kill -9 <pid_returned_from_previous_command>
# 	OR Alternatively give it a random port from the script that calls run_experiment_xpir.sh

if [ ! -d $RESULTS_DIRECTORY ]; then
	mkdir $RESULTS_DIRECTORY 
fi

if [ ! -d $RESULTS_PERCY_DIRECTORY ]; then
	mkdir $RESULTS_PERCY_DIRECTORY 
fi

cd $path_to_repos
if [ -d $PERCY_DIRECTORY ]; then
	echo "Folder Found for PERCY!"
else
	echo "Error : PERCY Folder not found"
	exit
fi

#PY_PARSE_CLIENTLOG="python ./extract_time_xpir_client.py "$XPIR_CLIENT_LOCATION" "$CLIENTLOG_FILENAME" "$XPIR_TIME_EXTRACT_TEMPFILE 
#PY_PARSE_SERVERLOG="python ./extract_time_xpir_server.py "$XPIR_SERVER_LOCATION" "$SERVERLOG_FILENAME" "$XPIR_TIME_EXTRACT_TEMPFILE_LOCATION" "$XPIR_TIME_EXTRACT_TEMPFILE" "$RESULTS_XPIR_PATH" "$CSV_FILE_NAME" "$bulk_batch_size

cd $PERCY_LOCATION
no_of_relays=$no_of_relays_start

while [ "$no_of_relays" -le "$no_of_relays_stop" ]
	do
	r=$no_of_relays
	b=$block_size
	#Need a string with a list of random numbers which will be provided as a part of the client command.
	#if [ "$no_of_relays" -gt 48000 ]
	#then
	#	r=$((r/2))
	#	b=$((b*2))			
	#fi
		
	DATABASE_SIZE_IN_BYTES=$((r*b))
	CREATE_DB_COMMAND="dd if=/dev/zero of="$DATABASE_FILENAME" bs="$DATABASE_SIZE_IN_BYTES" count=1"
	DELETE_DB_COMMAND="rm -f $DATABASE_FILENAME"
	DELETE_CLIENTLOG="rm -f $CLIENTLOG_FILENAME"

	PERCY_SERVER1_COMMAND="./pirserver "$DATABASE_FILENAME" 1 "$r" "$b" -w 1 -m c -p 30001 -H -l "$SERVER1LOG_FILENAME
	PERCY_SERVER2_COMMAND="./pirserver "$DATABASE_FILENAME" 2 "$r" "$b" -w 1 -m c -p 30002 -H -l "$SERVER2LOG_FILENAME
	PERCY_SERVER3_COMMAND="./pirserver "$DATABASE_FILENAME" 3 "$r" "$b" -w 1 -m c -p 30003 -H -l "$SERVER3LOG_FILENAME

	$CREATE_DB_COMMAND

	$PERCY_SERVER1_COMMAND 2>&1 &
	kill_id_server1=$!
	sleep 1s
	$PERCY_SERVER2_COMMAND 2>&1 &
	kill_id_server2=$!
	sleep 1s
	$PERCY_SERVER3_COMMAND 2>&1 &	
	kill_id_server3=$!
	sleep 1s

	counter=0 
	STRING_OF_RANDOM_INDEXES=""


	while [ $counter != $no_of_requests ]
		do
		#NOTE: $RANDOM returns a random number between 0 and 32767, so this is poor for r > 32767
		temp=$((($RANDOM%r)))
		#STRING_OF_RANDOM_INDEXES=$STRING_OF_RANDOM_INDEXES$temp
		#if [ $counter != $(($no_of_requests-1)) ]
		#then
		#	STRING_OF_RANDOM_INDEXES=$STRING_OF_RANDOM_INDEXES" "
		#fi
	
		#$PERCY_CLIENT_COMMAND
		./pirclient $r $b "1:localhost:30001 2:localhost:30002 3:localhost:30003" 2 "$temp" -w 1 -m c -H -l $CLIENTLOG_FILENAME
		counter=$((counter+1))
		done	
	#echo "STRING_OF_RANDOM_INDEXES = "$STRING_OF_RANDOM_INDEXES

	#STRING OF RANDOM INDEXES needs to be $bulk_batch_size long
	#PERCY_CLIENT_COMMAND='./pirclient '$r' '$b' "1:localhost:30001 2:localhost:30002 3:localhost:30003" 2 "'$STRING_OF_RANDOM_INDEXES'" -w 1 -m c -H -l '$CLIENTLOG_FILENAME  

	CSV_FILE_NAME="PERCY_"$no_of_relays"_"$block_size	

	sleep 2s	
	

	sleep 1s
	KILL_COMMAND="kill -9 $kill_id_server1"
	$KILL_COMMAND
	KILL_COMMAND="kill -9 $kill_id_server2"
	$KILL_COMMAND
	KILL_COMMAND="kill -9 $kill_id_server3"
	$KILL_COMMAND
	$DELETE_DB_COMMAND
	sleep 1s

	#Run Log Parser
	cd $SUBSCRIPT_FOLDER
	#PARSER_COMMAND
	python extract_time_percy.py $PERCY_LOCATION$CLIENTLOG_FILENAME $RESULTS_ITPIR_PATH$CSV_FILE_NAME
	
	#cp $CLIENTLOG_FILENAME $RESULTS_ITPIR_PATH$CSV_FILE_NAME
	cd $PERCY_LOCATION
	#$DELETE_CLIENTLOG	
	
	no_of_relays=$((no_of_relays+increment))
	#PARSE LOG FILE TO STORE THE RESULT FILE!
	done
	


