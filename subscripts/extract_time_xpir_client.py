import sys

#Receive these both as command line arguments !
# '/home/ssasy/Projects/XPIR/_build/apps/client/clientlog'
INPUT_FILELOCATION = str(sys.argv[1])
# '/home/ssasy/Projects/ConsenSGX/Scripts/time_round'
INPUT_FILENAME = str(sys.argv[2])
OUT_FILENAME = str(sys.argv[3])

time1=0
time2=0
single_qe_size=0
query_size=0
response_size=0
with open(INPUT_FILELOCATION+INPUT_FILENAME, 'r') as file_handle:
	for line in file_handle:
		words = line.split(' ')
		if(words[0]=="consensgx1"):
			time1 = words[-2].strip()
		if(words[0]=="consensgx2"):
			time2 = words[-2].strip()
		words=line.split(":")
		if(words[0]=="measure_size"):
			#single_qe_size=int(words[-2])
			#Modified to compute total query size in XPIR client, so directly use the value optained in log
			query_size = int(words[-2])
		if(words[0]=="measure_params"):
			alpha = words[-3]
			#n = int((words[-1].split(","))[0])
			#d = int((words[3]))
			#print(d)
			#print(n)
			#query_size = (n**d) * single_qe_size
			#print(single_qe_size)
			#print(query_size)
		if(words[0]=="measure_response_size"):
			response_size=words[1].strip()

#File format for XPIR is <GenerateQuery_time, ExtractResult_time, Query_size, Response_size, ProcessQuery_time>
with open(OUT_FILENAME, 'a') as file_handle:
	file_handle.write(str(time1)+','+ str(time2)+','+ str(query_size)+','+str(response_size)+','+'\n')


