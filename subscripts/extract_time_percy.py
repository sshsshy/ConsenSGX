import sys

#Receive these both as command line arguments !
# '/home/ssasy/Projects/XPIR/_build/apps/client/clientlog'
INPUT_FILENAME = str(sys.argv[1])
# '/home/ssasy/Projects/ConsenSGX/Scripts/time_round'
OUTPUT_FILENAME = str(sys.argv[2])

file_handle = open(INPUT_FILENAME, 'r')
lineList = file_handle.readlines()
file_handle.close()

file_handle = open(OUTPUT_FILENAME, 'w')

ctr=0
for line in lineList:
	if(ctr!=0):
		words = line.split(',')
		encode_time = words[10]
		request_size = words[12]
		server_time = words[13]
		response_size = words[15]
		decode_time = words[16]
		out_line = encode_time+','+request_size+','+server_time+','+response_size+','+decode_time+'\n' 
		file_handle.write(out_line)
	ctr=ctr+1	
file_handle.close()
