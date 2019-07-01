import sys

LOG_FILE = str(sys.argv[1])
OUT_FILE = str(sys.argv[2])
request_size=0
response_size=0

log_file_handle = open(OUT_FILE,'w')
with open(LOG_FILE, 'r') as log_file_handle:
	for line in log_file_handle:
		words=line.split(":")
		if(words[0]=="request_size"):
			request_size=words[1]
			response_size=words[3]

with open(OUT_FILE, 'w') as out_file_handle:
	out_file_handle.write(str(request_size)+','+str(response_size)+'\n')
