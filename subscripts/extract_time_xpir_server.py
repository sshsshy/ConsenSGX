import sys

#Receive these both as command line arguments !
# '/home/ssasy/Projects/XPIR/_build/apps/client/clientlog'
INPUT_FILELOCATION = str(sys.argv[1])
# '/home/ssasy/Projects/ConsenSGX/Scripts/time_round'
INPUT_FILENAME = str(sys.argv[2])
INTERMEDIATE_FILELOCATION = str(sys.argv[3])
INTERMEDIATE_FILENAME = str(sys.argv[4])
OUT_FILELOCATION = str(sys.argv[5])
OUT_FILENAME = str(sys.argv[6])
BULK_BATCH_SIZE = int(sys.argv[7])

query_process_time = []
query_generate_time = []
extract_response_time = []
lines=[]

with open(INPUT_FILELOCATION+INPUT_FILENAME, 'r') as file_handle:
	for line in file_handle:
		words = line.split(' ')
		if(words[0]=="consensgx"):
			query_process_time.append(float(words[-2].strip()))

#File format for XPIR is <GenerateQuery_time, ExtractResult_time, Request_size, Response_size, ProcessQuery_time>
with open(INTERMEDIATE_FILELOCATION + INTERMEDIATE_FILENAME, 'r') as file_handle:
	for line in file_handle:
		lines.append(line.strip())
		words = line.split(',')
		#query_generate_time.append(words[0])
		#extract_response_time.append(words[1])
	

print(query_process_time)
n=len(query_process_time)
print("Number of requests = "+str(n))
with open(OUT_FILELOCATION + OUT_FILENAME, 'w') as file_handle:
	
	if(BULK_BATCH_SIZE!=0):	
		for i in range(0,n):	
			#line = str(query_generate_time[i])+','+ str(query_process_time[i])+',' + str(extract_response_time[i])
			line = lines[i].strip()
			words = line.split(',')
			words_bulk = []
			line_bulk = ''
			for j in range(len(words)-1):
				words_bulk.append(float(words[j].strip()) * BULK_BATCH_SIZE)
				line_bulk = line_bulk + (str(words_bulk[j])+',')
			line_bulk = line_bulk +str(BULK_BATCH_SIZE * query_process_time[i]) + str('\n')			
			file_handle.write(line_bulk)
	else:
		for i in range(0,n):
			line = lines[i].strip()+str(query_process_time[i])+'\n'
			file_handle.write(line)

#Refresh the Intermediate file for future executions
file_temp = open(INTERMEDIATE_FILELOCATION + INTERMEDIATE_FILENAME, 'w')
file_temp.close()

file_temp = open(INPUT_FILELOCATION + INPUT_FILENAME, 'w')
file_temp.close()
