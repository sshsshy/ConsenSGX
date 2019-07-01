
import sys

#Receive as command line argument filename
FILENAME_IP = str(sys.argv[1]) 
FILENAME_OP = str(sys.argv[2])
N = str(sys.argv[3])

sum_term = 0
no_of_values = 0
with open(FILENAME_IP, 'r') as file_handle:
	for line in file_handle:
		val = float(line.strip())
		sum_term+=val
		no_of_values+=1

avg = sum_term/no_of_values
print(avg)

with open(FILENAME_OP, 'a') as file_handle:
	file_handle.write(str(N)+','+str(avg)+'\n')
