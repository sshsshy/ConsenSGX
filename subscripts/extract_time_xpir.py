import sys

#Receive these both as command line arguments !
# '/home/ssasy/Projects/XPIR/_build/apps/client/clientlog'
INPUT_FILENAME = str(sys.argv[1])
# '/home/ssasy/Projects/ConsenSGX/Scripts/time_round'
APPEND_FILENAME = str(sys.argv[2])

file_handle = open(INPUT_FILENAME, 'r')
lineList = file_handle.readlines()
file_handle.close()

words = lineList[-2].split()
#print words[-2]

file_handle = open(APPEND_FILENAME, 'a')
file_handle.write(words[-2] + '\n')
file_handle.close()


