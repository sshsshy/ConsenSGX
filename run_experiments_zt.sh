#!/bin/bash


if [ $# -ne 7 ]; then
	echo "Incorrect number of arguments. Expected : "
	echo "./run_experiments <no_of_relays/files start_value> <no_of_relays/files stop_value> <increment_multiplier> <block_size> <no_of_requests> <bulk_batch_size> <Full path to XPIR/ZT repos including trailing />"
fi

no_of_relays_start=$1
no_of_relays_stop=$2
increment=$3
block_size=$4
no_of_requests=$5
BULK_BATCH_SIZE=$6
path_to_repos=$7
pipe=/tmp/testpipe
START_PATH=$PWD"/"
SUBSCRIPT_FOLDER=$START_PATH"subscripts/"
RESULTS_ZT_PATH=$START_PATH"Results/ZT/"

if [[ ! -p $pipe ]]; then
	mkfifo $pipe
fi


echo
echo
echo "ZeroTrace:"
echo

ZT_DIRECTORY=$path_to_repos"ZeroTrace"
RESULTS_DIRECTORY="Results"
RESULTS_ZT_DIRECTORY="Results/ZT"
STASH_SIZE=10
DATA_SIZE=$block_size
RECURSION_BLOCK_SIZE=64
Z=4
ZT_LOG_LOCATION=$SUBSCRIPT_FOLDER"ZT_log.txt"
ZT_TIMING_LOCATION=$SUBSCRIPT_FOLDER"Timing_ZT.csv"

# <N> <No_of_requests> <Stash_size> <Data_block_size> <\"resume\"/\"new\"> <\"memory\"/\"hdd\"> <0/1 = Non-oblivious/Oblivious> <Recursion_block_size> <\"auto\"/\"path\"/\"circuit\"> <Z>

if [ ! -d $RESULTS_DIRECTORY ]; then
	mkdir $RESULTS_DIRECTORY 
fi

if [ ! -d $RESULTS_ZT_DIRECTORY ]; then
	mkdir $RESULTS_ZT_DIRECTORY 
fi

if [ -d $ZT_DIRECTORY ]; then
	echo "Folder Found for ZeroTrace!"
else
	echo "Error : ZeroTrace Folder not found"
	exit
fi
cd $ZT_DIRECTORY
echo

echo "Compiling ZeroTrace..."
make>make_log.txt
echo

no_of_relays=$no_of_relays_start
while [ "$no_of_relays" -le "$no_of_relays_stop" ]
	do
		cd $ZT_DIRECTORY
		ZT_COMMAND="./Sample_App/sampleapp "$no_of_relays" "$no_of_requests" "$STASH_SIZE" "$DATA_SIZE" new memory 1 "$RECURSION_BLOCK_SIZE" circuit "$Z" "$BULK_BATCH_SIZE
		RESULTS_FILE_NAME="ZT_"$no_of_relays"_"$DATA_SIZE"_"$BULK_BATCH_SIZE
		echo "Executing :"
		echo $ZT_COMMAND 
		$ZT_COMMAND>$ZT_LOG_LOCATION
		cp $RESULTS_FILE_NAME $RESULTS_ZT_PATH
		echo
		cd $SUBSCRIPT_FOLDER
		ZT_EXTRACT_SIZES="python ./extract_sizes_zt.py "$ZT_LOG_LOCATION" "$RESULTS_ZT_PATH$RESULTS_FILE_NAME"_sizes"
		$ZT_EXTRACT_SIZES

		no_of_relays=$((no_of_relays+increment))
	done





#Parse ZT_log.txt , fetch query time from last line
#cd $SUBSCRIPT_FOLDER
#PY_COMMAND="python ./extract_time_zt.py "$ZT_LOG_LOCATION" "$ZT_TIMING_LOCATION" "$N" "$DATA_SIZE
#$PY_COMMAND


