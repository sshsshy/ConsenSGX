import sys
import subprocess
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit
from operator import add
import operator

#NOTE: Setup Bulk Batches list
BULK_BATCH_SIZES=[10, 50]

def quadratic_function(x, a, b, c):
    return a*x*x + b*x + c

def linear_function(x, a, b):
    return a*x + b

FOLDER_XPIR = 'Results/XPIR/'
FOLDER_ZT = 'Results/ZT/'
FOLDER_PERCY = 'Results/Percy/'

RELAYS_START=int(sys.argv[1])
RELAYS_STOP=int(sys.argv[2])
RELAYS_INCREMENT=int(sys.argv[3])
BLOCK_SIZE=int(sys.argv[4])
NO_OF_REQ=int(sys.argv[5])

# 2MB for 6300 relays
TOR_MICRODESCRIPTOR_CONSENSUS_SIZE_PER_RELAY = float(2000000)/float(6300)
TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY = float(98723)/float(6300)


ZT_QE_TIME={}
ZT_RE_TIME={}
ZT_PQ_TIME={}
ZT_REQUEST_SIZE={}
ZT_RESPONSE_SIZE={}
ZT_QE_STD={}
ZT_RE_STD={}
ZT_PQ_STD={}
ZT_CLIENT_TIME={}
ZT_CLIENT_STD={}

XPIR_QE_TIME={}
XPIR_RE_TIME={}
XPIR_PQ_TIME={}
XPIR_REQUEST_SIZE={}
XPIR_RESPONSE_SIZE={}
XPIR_QE_STD={}
XPIR_RE_STD={}
XPIR_PQ_STD={}
XPIR_CLIENT_TIME={}
XPIR_CLIENT_STD={}

PERCY_QE_TIME={}
PERCY_RE_TIME={}
PERCY_PQ_TIME={}
PERCY_REQUEST_SIZE={}
PERCY_RESPONSE_SIZE={}
PERCY_QE_STD={}
PERCY_RE_STD={}
PERCY_PQ_STD={}
PERCY_CLIENT_TIME={}
PERCY_CLIENT_STD={}

N = []

POINT_STYLES = [".","v","s","+","x","d",">","^","*","o","D"]

#Process ZT Results

for bulk_batch_size in BULK_BATCH_SIZES:
	current_relays=RELAYS_START
	N=[]

	ZT_QE_TIME[bulk_batch_size] = []
	ZT_RE_TIME[bulk_batch_size]=[]
	ZT_PQ_TIME[bulk_batch_size]=[]
	ZT_REQUEST_SIZE[bulk_batch_size]=[]
	ZT_RESPONSE_SIZE[bulk_batch_size]=[]
	ZT_QE_STD[bulk_batch_size]=[]
	ZT_RE_STD[bulk_batch_size]=[]
	ZT_PQ_STD[bulk_batch_size]=[]
	ZT_CLIENT_TIME[bulk_batch_size]=[]
	ZT_CLIENT_STD[bulk_batch_size]=[]
	#<QueryGen_time, ProcessRequest_time, ReplyExtract_time>
	while(current_relays<=RELAYS_STOP):
		FILE_NAME_TIME=FOLDER_ZT+"ZT_"+str(current_relays)+"_"+str(BLOCK_SIZE)+"_"+str(bulk_batch_size)
		FILE_NAME_SIZE=FILE_NAME_TIME+"_sizes"
		qe_time=[]
		re_time=[]
		pq_time=[]
		client_time=[]	
		request_size=0
		response_size=0
		with open(FILE_NAME_TIME,'r') as file_handle:
			ctr=0
			for line in file_handle:
				if(ctr!=0):
					words=line.split('\t')
					qe_time.append(float(words[0]))	
					pq_time.append(float(words[1]))
					re_time.append(float(words[2]))
					client_time.append(float(words[0])+float(words[2]))
				ctr=ctr+1
		with open(FILE_NAME_SIZE,'r') as file_handle:
			line = file_handle.readline()
			words = line.split(",")
			request_size=int(words[0])
			response_size=int(words[1])

		ZT_REQUEST_SIZE[bulk_batch_size].append(request_size)
		ZT_RESPONSE_SIZE[bulk_batch_size].append(response_size)
		ZT_QE_TIME[bulk_batch_size].append(np.mean(qe_time))
		ZT_PQ_TIME[bulk_batch_size].append(np.mean(pq_time))
		ZT_RE_TIME[bulk_batch_size].append(np.mean(re_time))
		ZT_CLIENT_TIME[bulk_batch_size].append(np.mean(client_time))
		ZT_QE_STD[bulk_batch_size].append(np.std(qe_time))
		ZT_PQ_STD[bulk_batch_size].append(np.std(pq_time))
		ZT_RE_STD[bulk_batch_size].append(np.std(re_time))
		ZT_CLIENT_STD[bulk_batch_size].append(np.std(client_time))

		N.append(current_relays)
		current_relays=current_relays+RELAYS_INCREMENT


#Process XPIR Results
#<QueryGen_time, ReplyExtract_time, Request_size, Response_size, ProcessRequest_time>


for bulk_batch_size in BULK_BATCH_SIZES:
	XPIR_QE_TIME[bulk_batch_size]=[]
	XPIR_RE_TIME[bulk_batch_size]=[]
	XPIR_PQ_TIME[bulk_batch_size]=[]
	XPIR_REQUEST_SIZE[bulk_batch_size]=[]
	XPIR_RESPONSE_SIZE[bulk_batch_size]=[]
	XPIR_QE_STD[bulk_batch_size]=[]
	XPIR_RE_STD[bulk_batch_size]=[]
	XPIR_PQ_STD[bulk_batch_size]=[]
	XPIR_CLIENT_TIME[bulk_batch_size]=[]
	XPIR_CLIENT_STD[bulk_batch_size]=[]

	current_relays=RELAYS_START
	while(current_relays<=RELAYS_STOP):
		FILE_NAME=FOLDER_XPIR+"XPIR_"+str(current_relays)+"_"+str(BLOCK_SIZE)+"_"+str(bulk_batch_size)
		qe_time=[]
		re_time=[]
		pq_time=[]
		client_time=[]
		request_size=0
		response_size=0
		with open(FILE_NAME,'r') as file_handle:
			ctr=0
			for line in file_handle:
				if(ctr!=0):
					words=line.split(',')
					qe_time.append(float(words[0]))	
					pq_time.append(float(words[4]))
					re_time.append(float(words[1]))
					client_time.append(float(words[0])+float(words[1]))
					request_size=(float(words[2]))
					response_size=(float(words[3]))
				ctr=ctr+1			

		XPIR_REQUEST_SIZE[bulk_batch_size].append(request_size)
		XPIR_RESPONSE_SIZE[bulk_batch_size].append(response_size)
		XPIR_QE_TIME[bulk_batch_size].append(np.mean(qe_time))
		XPIR_PQ_TIME[bulk_batch_size].append(np.mean(pq_time))
		XPIR_RE_TIME[bulk_batch_size].append(np.mean(re_time))
		XPIR_CLIENT_TIME[bulk_batch_size].append(np.mean(client_time))
		XPIR_QE_STD[bulk_batch_size].append(np.std(qe_time))
		XPIR_PQ_STD[bulk_batch_size].append(np.std(pq_time))
		XPIR_RE_STD[bulk_batch_size].append(np.std(re_time))
		XPIR_CLIENT_STD[bulk_batch_size].append(np.std(client_time))
		current_relays=current_relays+RELAYS_INCREMENT	

print(XPIR_PQ_TIME)
print(XPIR_PQ_STD)
print(XPIR_CLIENT_TIME)

print("ZT_CLIENT_TIME:")
print(ZT_CLIENT_TIME)

#Process Percy Results
#<QueryGen_time,  Request_size, ProcessRequest_time, Response_size, ResponseExtract_time>
#NOTE: Unit for time is seconds and size in bytes for Percy

for bulk_batch_size in BULK_BATCH_SIZES:
	PERCY_QE_TIME[bulk_batch_size]=[]
	PERCY_RE_TIME[bulk_batch_size]=[]
	PERCY_PQ_TIME[bulk_batch_size]=[]
	PERCY_REQUEST_SIZE[bulk_batch_size]=[]
	PERCY_RESPONSE_SIZE[bulk_batch_size]=[]
	PERCY_QE_STD[bulk_batch_size]=[]
	PERCY_RE_STD[bulk_batch_size]=[]
	PERCY_PQ_STD[bulk_batch_size]=[]
	PERCY_CLIENT_TIME[bulk_batch_size]=[]
	PERCY_CLIENT_STD[bulk_batch_size]=[]

	current_relays=RELAYS_START
	while(current_relays<=RELAYS_STOP):
		FILE_NAME=FOLDER_PERCY+"PERCY_"+str(current_relays)+"_"+str(BLOCK_SIZE)
		qe_time=[]
		re_time=[]
		pq_time=[]
		client_time=[]
		request_size=0
		response_size=0
		with open(FILE_NAME,'r') as file_handle:
			ctr=0
			for line in file_handle:
				if(ctr!=0):
					words=line.split(',')
					qe_time.append(float(words[0]) * bulk_batch_size)	
					pq_time.append(float(words[2]) * bulk_batch_size)
					re_time.append(float(words[4]) * bulk_batch_size)
					client_time.append( (float(words[0])+float(words[4]))  * bulk_batch_size)
					request_size=(float(words[1]) * bulk_batch_size)
					response_size=(float(words[3]) * bulk_batch_size)
				ctr=ctr+1			

		# *3 hack because IT-PIR client log doesnt account for bandwidth to send to the 3 servers, although response log accounts for it!
		PERCY_REQUEST_SIZE[bulk_batch_size].append(request_size*3)
		PERCY_RESPONSE_SIZE[bulk_batch_size].append(response_size)
		#NOTE * 1000, to convert from sec to ms!
		PERCY_QE_TIME[bulk_batch_size].append(np.mean(qe_time) * 1000)
		PERCY_PQ_TIME[bulk_batch_size].append(np.mean(pq_time) * 1000)
		PERCY_RE_TIME[bulk_batch_size].append(np.mean(re_time) * 1000)
		PERCY_CLIENT_TIME[bulk_batch_size].append(np.mean(client_time) * 1000)
		PERCY_QE_STD[bulk_batch_size].append(np.std(qe_time) * 1000)
		PERCY_PQ_STD[bulk_batch_size].append(np.std(pq_time) * 1000)
		PERCY_RE_STD[bulk_batch_size].append(np.std(re_time) * 1000)
		PERCY_CLIENT_STD[bulk_batch_size].append(np.std(client_time) * 1000)
		current_relays=current_relays+RELAYS_INCREMENT	

print("PERCY_CLIENT_TIME:")
print(PERCY_CLIENT_TIME)
######

N_np = np.array(N)

plt.xlabel('Number of Relays')
plt.ylabel('Client computation time per query (in ms)')
plt.grid(True)
#plt.ylim( (pow(10,-1),pow(10,6.5)) )
plt.yscale('log')

line_xpir=[]
line_zt=[]

c_ctr = 0
for bulk_batch_size in BULK_BATCH_SIZES:
	
	XPIR_CLIENT_TIME_np = np.array(XPIR_CLIENT_TIME[bulk_batch_size])
	ZT_CLIENT_TIME_np = np.array(ZT_CLIENT_TIME[bulk_batch_size])
	PERCY_CLIENT_TIME_np = np.array(PERCY_CLIENT_TIME[bulk_batch_size])

	params_xpir = curve_fit(linear_function, N_np, XPIR_CLIENT_TIME_np)
	params_zt = curve_fit(linear_function, N_np, ZT_CLIENT_TIME_np)
	params_percy = curve_fit(linear_function, N_np, PERCY_CLIENT_TIME_np)

	x = np.arange(min(N),max(N))
	a,b = params_xpir[0]
	#y_xpir = quadratic_function(x, a, b, c)
	y_xpir = linear_function(x, a, b)
	a,b = params_zt[0]
	y_zt = linear_function(x, a, b)
	a,b = params_percy[0]
	y_percy = linear_function(x, a, b)

	#Feed X and Y points to points1, points2
	#line_xpir=plt.plot(x, y_xpir, '--', color = str("C")+str(c_ctr), label='XPIR, B=' + str(bulk_batch_size))
	#line_zt=plt.plot(x, y_zt, '-', color =str("C")+str(c_ctr+1), label='ZT, B=' + str(bulk_batch_size))
	#line_percy=plt.plot(x, y_percy, '-.', color =str("C")+str(c_ctr+2), label='Percy, B=' + str(bulk_batch_size))

	points1 = plt.plot(N, XPIR_CLIENT_TIME[bulk_batch_size], POINT_STYLES[c_ctr], label='XPIR, B='+ str(bulk_batch_size), color = str("C")+str(c_ctr) ) 
	points2 = plt.plot(N, PERCY_CLIENT_TIME[bulk_batch_size], POINT_STYLES[c_ctr+1], label='Chor-XOR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+1) )
	points3 = plt.plot(N, ZT_CLIENT_TIME[bulk_batch_size], POINT_STYLES[c_ctr+2], label='ZT, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+2) )
	
	errbar1 = plt.errorbar(N, XPIR_CLIENT_TIME[bulk_batch_size], XPIR_CLIENT_STD[bulk_batch_size],None,'r',ls='none',mew=3)
	errbar2 = plt.errorbar(N, PERCY_CLIENT_TIME[bulk_batch_size], PERCY_CLIENT_STD[bulk_batch_size],None,'r',ls='none',mew=3)
	errbar3 = plt.errorbar(N, ZT_CLIENT_TIME[bulk_batch_size], ZT_CLIENT_STD[bulk_batch_size],None,'r',ls='none',mew=3)


	plt.setp(points1, 'mew', '3.0')
	plt.setp(points2, 'mew', '3.0')
	plt.setp(points3, 'mew', '3.0')
	#plt.setp(line_xpir, 'linewidth', '2.0')
	#plt.setp(line_zt, 'linewidth', '2.0')
	c_ctr+=3

ax = plt.subplot()
handles, labels = ax.get_legend_handles_labels()
labels_sort = [2,4,6,1,3,5]
hl = sorted(zip(handles, labels, labels_sort),
            key=operator.itemgetter(2))
handles2, labels2, labels_sort= zip(*hl)
#ax.legend(handles2, labels2, loc = 7)


#plt.legend(line_xpir[BULK_BATCH_SIZE[2]],line_xpir[BULK_BATCH_SIZE[1]],line_xpir[BULK_BATCH_SIZE[0]],line_zt[BULK_BATCH_SIZE[2]],line_zt[BULK_BATCH_SIZE[1]],line_zt[BULK_BATCH_SIZE[0]])
plt.title('Client computation time (in ms) vs number of relays')
ax.legend(handles2, labels2, loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=2, shadow=True)
plt.savefig('client_time.png', bbox_inches='tight')
plt.close()

###############

plt.xlabel('Number of Relays')
plt.ylabel('Server computation time per query (in ms)')
plt.grid(True)
plt.yscale('log')

c_ctr = 0
for bulk_batch_size in BULK_BATCH_SIZES:

	XPIR_PQ_TIME_np = np.array(XPIR_PQ_TIME[bulk_batch_size])
	ZT_PQ_TIME_np = np.array(ZT_PQ_TIME[bulk_batch_size])
	PERCY_PQ_TIME_np = np.array(PERCY_PQ_TIME[bulk_batch_size])

	params_xpir = curve_fit(quadratic_function, N_np, XPIR_PQ_TIME_np)
	params_zt = curve_fit(quadratic_function, N_np, ZT_PQ_TIME_np)
	params_percy = curve_fit(quadratic_function, N_np, PERCY_PQ_TIME_np)

	x = np.arange(min(N),max(N))
	a,b,c = params_xpir[0]
	y_xpir = quadratic_function(x, a, b, c)
	#y_xpir = linear_function(x, a, b)
	a,b,c = params_zt[0]
	y_zt = quadratic_function(x, a, b, c)
	a,b,c = params_percy[0]
	y_percy = quadratic_function(x, a, b, c)

	#Feed X and Y points to points1, points2
	#line1 = plt.plot(x, y_xpir, '--', color = str("C")+str(c_ctr), label='XPIR, B=' + str(bulk_batch_size))
	#line2 = plt.plot(x, y_zt, '-', color = str("C")+str(c_ctr+1), label='ZT, B=' + str(bulk_batch_size))
	#line3 = plt.plot(x, y_percy, '-', color = str("C")+str(c_ctr+1), label='Percy, B=' + str(bulk_batch_size))

	points1 = plt.plot(N, XPIR_PQ_TIME[bulk_batch_size], POINT_STYLES[c_ctr],label='XPIR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr))
	points2 = plt.plot(N, PERCY_PQ_TIME[bulk_batch_size], POINT_STYLES[c_ctr+1],label='Chor-XOR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+1))
	points2 = plt.plot(N, ZT_PQ_TIME[bulk_batch_size], POINT_STYLES[c_ctr+2],label='ZT, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+2))

	errbar1 = plt.errorbar(N, XPIR_PQ_TIME[bulk_batch_size], XPIR_PQ_STD[bulk_batch_size],None,'r',ls='none',mew=3)
	errbar2 = plt.errorbar(N, PERCY_PQ_TIME[bulk_batch_size], PERCY_PQ_STD[bulk_batch_size],None,'r',ls='none',mew=3)
	errbar3 = plt.errorbar(N, ZT_PQ_TIME[bulk_batch_size], ZT_PQ_STD[bulk_batch_size],None,'r',ls='none',mew=3)

	plt.setp(points1, 'mew', '3.0')
	plt.setp(points2, 'mew', '3.0')
	plt.setp(points3, 'mew', '3.0')
	#plt.setp(line1, 'linewidth', '2.0')
	#plt.setp(line2, 'linewidth', '2.0')
	c_ctr+=3

ax = plt.subplot()
handles, labels = ax.get_legend_handles_labels()
labels_sort = [2,4,6,1,3,5]
hl = sorted(zip(handles, labels, labels_sort),
            key=operator.itemgetter(2))
handles2, labels2, labels_sort= zip(*hl)
#ax.legend(handles2, labels2, loc = 7)

plt.title('Server computation time (in ms) vs number of relays')
ax.legend(handles2, labels2, loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=2, shadow=True)
plt.savefig('server_time.png', bbox_inches='tight')
plt.close()

################

c_ctr = 0
for bulk_batch_size in BULK_BATCH_SIZES:

	XPIR_REQUEST_SIZE_np = np.array(XPIR_REQUEST_SIZE[bulk_batch_size])
	ZT_REQUEST_SIZE_np = np.array(ZT_REQUEST_SIZE[bulk_batch_size])
	PERCY_REQUEST_SIZE_np = np.array(PERCY_REQUEST_SIZE[bulk_batch_size])

	params_xpir = curve_fit(linear_function, N_np, XPIR_REQUEST_SIZE_np)
	params_zt = curve_fit(linear_function, N_np, ZT_REQUEST_SIZE_np)
	params_percy = curve_fit(linear_function, N_np, PERCY_REQUEST_SIZE_np)

	x = np.arange(min(N),max(N))
	a,b = params_xpir[0]
	#y_xpir = quadratic_function(x, a, b, c)
	y_xpir = linear_function(x, a, b)
	a,b = params_zt[0]
	y_zt = linear_function(x, a, b)
	a,b = params_percy[0]
	y_percy = linear_function(x, a, b)

	#x1, y1 = [min(N), max(N)], [ZT_REQUEST_SIZE[0], ZT_REQUEST_SIZE[0]]
	#line2 = plt.plot(x1, y1, color = 'g')

	#line1 = plt.plot(x, y_xpir, '--', color = str("C")+str(c_ctr),  label='XPIR, B=' + str(bulk_batch_size))	
	#line2 = plt.plot(x, y_percy, '-',  color = str("C")+str(c_ctr+1),  label='Percy, B=' + str(bulk_batch_size))
	#line3 = plt.plot(x, y_zt, '-',  color = str("C")+str(c_ctr+2),  label='ZT, B=' + str(bulk_batch_size))

	points1 = plt.plot(N, XPIR_REQUEST_SIZE[bulk_batch_size], POINT_STYLES[c_ctr], label='XPIR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr))
	points2 = plt.plot(N, PERCY_REQUEST_SIZE[bulk_batch_size], POINT_STYLES[c_ctr+1], label='Chor-XOR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+1))
	points3 = plt.plot(N, ZT_REQUEST_SIZE[bulk_batch_size], POINT_STYLES[c_ctr+2], label='ZT, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+2))

	plt.setp(points1, 'mew', '3.0')
	plt.setp(points2, 'mew', '3.0')
	plt.setp(points3, 'mew', '3.0')
	#plt.setp(line1, 'linewidth', '2.0')
	#plt.setp(line2, 'linewidth', '2.0')
	#plt.setp(line3, 'linewidth', '2.0')
	c_ctr+=3

ax = plt.subplot()
handles, labels = ax.get_legend_handles_labels()
labels_sort = [2,4,6,1,3,5]
hl = sorted(zip(handles, labels, labels_sort),
            key=operator.itemgetter(2))
handles2, labels2, labels_sort= zip(*hl)
ax.legend(handles2, labels2, loc = 7)


plt.xlabel('Number of Relays')
plt.ylabel('Request size (in bytes)')
plt.grid(True)
plt.yscale('log')
plt.title('Request sizes (in bytes) vs number of relays')
ax.legend(handles2, labels2, loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=2, shadow=True)
plt.savefig('request_size.png', bbox_inches='tight')
plt.close()

###################


c_ctr = 0
for bulk_batch_size in BULK_BATCH_SIZES:

	XPIR_RESPONSE_SIZE_np = np.array(XPIR_RESPONSE_SIZE[bulk_batch_size])
	ZT_RESPONSE_SIZE_np = np.array(ZT_RESPONSE_SIZE[bulk_batch_size])
	params_xpir = curve_fit(linear_function, N_np, XPIR_RESPONSE_SIZE_np)
	params_zt = curve_fit(linear_function, N_np, ZT_RESPONSE_SIZE_np)
	x = np.arange(min(N),max(N))
	a,b = params_xpir[0]
	#y_xpir = quadratic_function(x, a, b, c)
	y_xpir = linear_function(x, a, b)
	a,b = params_zt[0]
	y_zt = linear_function(x, a, b)

	#x1, y1 = [min(N), max(N)], [ZT_REQUEST_SIZE[0], ZT_REQUEST_SIZE[0]]
	#line2 = plt.plot(x1, y1, color = 'g')

	#line1 = plt.plot(x, y_xpir, '--', color = str("C")+str(c_ctr), label='XPIR, B=' + str(bulk_batch_size))
	#line2 = plt.plot(x, y_zt, '-', color = str("C")+str(c_ctr+1), label='ZT, B=' + str(bulk_batch_size))

	points1 = plt.plot(N, XPIR_RESPONSE_SIZE[bulk_batch_size],  POINT_STYLES[c_ctr], label='XPIR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr))
	points2 = plt.plot(N, PERCY_RESPONSE_SIZE[bulk_batch_size],  POINT_STYLES[c_ctr+1], label='Chor-XOR, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+1))
	points3 = plt.plot(N, ZT_RESPONSE_SIZE[bulk_batch_size],  POINT_STYLES[c_ctr+2], label='ZT, B=' + str(bulk_batch_size), color = str("C")+str(c_ctr+2))
	
	plt.setp(points1, 'mew', '3.0')
	plt.setp(points2, 'mew', '3.0')
	plt.setp(points3, 'mew', '3.0')
	#plt.setp(line1, 'linewidth', '2.0')
	#plt.setp(line2, 'linewidth', '2.0')
	c_ctr+=3	

MICRODESCRIPTOR_SIZE = [float((x*TOR_MICRODESCRIPTOR_CONSENSUS_SIZE_PER_RELAY)+(x*0.0149*660)) for x in N]
points4 = plt.plot(N, MICRODESCRIPTOR_SIZE,  POINT_STYLES[c_ctr], label='Tor Microdescriptor Consensus', color = str("C")+str(c_ctr))

c_ctr=c_ctr+1

MICRODESCRIPTOR_DIFF_SIZE = [float((x * TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY) + (x*0.0149*660)) for x in N]
points5 = plt.plot(N, MICRODESCRIPTOR_DIFF_SIZE,  POINT_STYLES[c_ctr], label='Diff of Tor Microdescriptor Consensus', color = str("C")+str(c_ctr))
plt.setp(points4, 'mew', '3.0')
plt.setp(points5, 'mew', '3.0')

print("Microdescriptor DIFF SIZES:")
print(MICRODESCRIPTOR_DIFF_SIZE)

ax = plt.subplot()
handles, labels = ax.get_legend_handles_labels()
labels_sort = [2,6,8,1,5,7,3,4]
hl = sorted(zip(handles, labels, labels_sort),
            key=operator.itemgetter(2))
handles2, labels2, labels_sort= zip(*hl)
#ax.legend(handles2, labels2, loc = 7)

plt.xlabel('Number of Relays')
plt.ylabel('Response size in bytes')
plt.grid(True)
plt.yscale('log')
plt.title('Response sizes (in bytes) vs number of relays')
ax.legend(handles2, labels2, loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=2, shadow=True)
plt.savefig('response_size.png', bbox_inches='tight')
plt.close()

######################


#1MB
#10MB
#divided by 1000 to convert to MBp(ms)

plt.xlabel('Number of Relays')
plt.ylabel('End-to-end time for single query(in ms)')
plt.grid(True)
plt.yscale('log')



#84 descriptor changes per epoch on average for 6300 relays
#So 1.492% relays change
#Average microdescriptor size = 0.66KB
#(Computed from microdescriptors_diff.py script)

#color_xpir = ['k','b']
#color_zt = ['y','g']

c_ctr=0
BULK_BATCH_SIZES_2 =[10,50]
#NETWORK_BANDWIDTH is treated as Megabits, so 2 Mbps
NETWORK_BANDWIDTH =[4]

for i in NETWORK_BANDWIDTH:

	for bulk_batch_size in BULK_BATCH_SIZES_2:
		WAN_BW=float(i*1000*1000)/1000
		XPIR_COMP_TIME = list(map(add, XPIR_CLIENT_TIME[bulk_batch_size], XPIR_PQ_TIME[bulk_batch_size]))
		XPIR_TT_STD = list(map(add, XPIR_CLIENT_STD[bulk_batch_size], XPIR_PQ_STD[bulk_batch_size]))
		XPIR_BW = list(map(add, XPIR_REQUEST_SIZE[bulk_batch_size], XPIR_RESPONSE_SIZE[bulk_batch_size]))
		#Divide by 8 since WAN_BW is in Mbps, but x is in bytes
		XPIR_NW_TIME= [float(x) / float(WAN_BW/8) for x in XPIR_BW]
		XPIR_TT = list(map(add, XPIR_COMP_TIME, XPIR_NW_TIME))

		#print(XPIR_COMP_TIME)
		#print(XPIR_NW_TIME)
		#print(XPIR_TT)

		ZT_COMP_TIME = list(map(add, ZT_CLIENT_TIME[bulk_batch_size], ZT_PQ_TIME[bulk_batch_size]))
		ZT_TT_STD = list(map(add, ZT_CLIENT_STD[bulk_batch_size], ZT_PQ_STD[bulk_batch_size]))
		ZT_BW = list(map(add, ZT_REQUEST_SIZE[bulk_batch_size], ZT_RESPONSE_SIZE[bulk_batch_size]))
		#Divide by 8 since WAN_BW is in Mbps, but x is in bytes
		ZT_NW_TIME = [float(x) / float(WAN_BW/8) for x in ZT_BW]
		ZT_TT = list(map(add, ZT_COMP_TIME, ZT_NW_TIME))
		
		PERCY_BW = list(map(add, PERCY_REQUEST_SIZE[bulk_batch_size], PERCY_RESPONSE_SIZE[bulk_batch_size]))
		PERCY_NW_TIME = [float(x) / float(WAN_BW/8) for x in PERCY_BW]
		PERCY_COMP_TIME = list(map(add, PERCY_CLIENT_TIME[bulk_batch_size], PERCY_PQ_TIME[bulk_batch_size]))
		PERCY_TT = list(map(add, PERCY_COMP_TIME, PERCY_NW_TIME))
		PERCY_TT_STD = list(map(add, PERCY_CLIENT_STD[bulk_batch_size], PERCY_PQ_STD[bulk_batch_size]))

		XPIR_TT_np = np.array(XPIR_TT)
		ZT_TT_np = np.array(ZT_TT)
		PERCY_TT_np = np.array(PERCY_TT)
		params_xpir = curve_fit(quadratic_function, N_np, XPIR_TT_np)
		params_zt = curve_fit(quadratic_function, N_np, ZT_TT_np)
		params_percy = curve_fit(quadratic_function, N_np, PERCY_TT_np)
		x = np.arange(min(N),max(N))
		a,b,c = params_xpir[0]
		y_xpir = quadratic_function(x, a, b, c)
		#y_xpir = linear_function(x, a, b)
		a,b,c = params_zt[0]
		y_zt = quadratic_function(x, a, b, c)

		#line1 = plt.plot(x, y_xpir, '-', label = 'XPIR'+' with WAN BW='+str(i)+" MBps, B="+str(bulk_batch_size), color = str("C")+str(c_ctr))
		#line2 = plt.plot(x, y_zt, '-', label = 'ZT'+' with WAN BW='+str(i)+" MBps, B="+str(bulk_batch_size), color = str("C")+str(c_ctr+1))

		points1 = plt.plot(N, XPIR_TT, POINT_STYLES[c_ctr], label = "XPIR, B="+str(bulk_batch_size), color = str("C")+str(c_ctr))
		points2 = plt.plot(N, PERCY_TT, POINT_STYLES[c_ctr+1], label = "Chor-XOR, B="+str(bulk_batch_size), color = str("C")+str(c_ctr+1))
		points3 = plt.plot(N, ZT_TT, POINT_STYLES[c_ctr+2], label = "ZT, B="+str(bulk_batch_size), color = str("C")+str(c_ctr+2))


		errbar1 = plt.errorbar(N, XPIR_TT, XPIR_TT_STD, None,'r',ls='none',mew=3)
		errbar2 = plt.errorbar(N, PERCY_TT, PERCY_TT_STD, None,'r',ls='none',mew=3)
		errbar3 = plt.errorbar(N, ZT_TT, ZT_TT_STD, None,'r',ls='none',mew=3)

		
		if(bulk_batch_size==50):
			print("XPIR_TT:")
			print(XPIR_TT)
			print("XPIR_TT_STD:")
			print(XPIR_TT_STD)
			print("PERCY_TT:")
			print(PERCY_TT)
			print("PERCY_TT_STD:")
			print(PERCY_TT_STD)
			print("ZT_TT:")
			print(ZT_TT)
			print("ZT_TT_STD:")
			print(ZT_TT_STD)
	
		plt.setp(points1, 'mew', '3.0')
		plt.setp(points2, 'mew', '3.0')
		plt.setp(points3, 'mew', '3.0')
		#plt.setp(line1, 'linewidth', '2.0')
		#plt.setp(line2, 'linewidth', '2.0')
		c_ctr+=3

#Plot Tor microdescriptor points
WAN_BW=float(NETWORK_BANDWIDTH[0]*1000*1000)/1000
#Divide by 8 since WAN_BW is in Mbps, but x is in bytes
MICRODESCRIPTOR_TIME = [float((x*TOR_MICRODESCRIPTOR_CONSENSUS_SIZE_PER_RELAY)+(x*0.0149*660))/float(WAN_BW/8) for x in N]
#print("MICRODESCRIPTOR_TIME:")
#print(MICRODESCRIPTOR_TIME)
points3 = plt.plot(N, MICRODESCRIPTOR_TIME, POINT_STYLES[c_ctr], label = 'Tor Microdescriptor Consensus', color = str("C")+str(c_ctr))
c_ctr+=1

#AVG Microdescriptor consensus diff per epoch(for 1 hour windows) 98.723000 KB
#print('TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY = '+str(TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY))
MICRODESCRIPTOR_DIFF_TIME = [float((x * TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY) + (x*0.0149*660))/float(WAN_BW/8) for x in N]
points4 = plt.plot(N, MICRODESCRIPTOR_DIFF_TIME, POINT_STYLES[c_ctr], label = 'Diff of Tor Microdescriptor Consensus', color = str("C")+str(c_ctr))

print("MICRODESCRIPTOR TIME:")
print(MICRODESCRIPTOR_TIME)

print("MICRODESCRIPTOR_DIFF_TIME:")
print(MICRODESCRIPTOR_DIFF_TIME)

MICRODESC_DIFF_SIZE= [float((x * TOR_MICRODESCRIPTOR_CONSENSUS_DIFF_SIZE_PER_RELAY) + (x*0.0149*660)) for x in N]
#print("Microdesc_diff_sizes in bytes : ")
#print(MICRODESC_DIFF_SIZE)
ax = plt.subplot()
handles, labels = ax.get_legend_handles_labels()
#labels_sort = [3,7,1,5,4,8,2,6]
labels_sort = [2,6,8,1,5,7,3,4]
hl = sorted(zip(handles, labels, labels_sort),
            key=operator.itemgetter(2))
handles2, labels2, labels_sort= zip(*hl)
#ax.legend(handles2, labels2, loc = 7)
plt.title('End-to-End time for a query with Tor guard nodes of 4 Mbps bandwidth')
ax.legend(handles2, labels2, loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=2, shadow=True)
plt.savefig('e2e.png', bbox_inches='tight')
plt.close()


######################
# Number of ConsenSGX caches required graph

PER_CLIENT_COMPUTATION_TIME=200 #ms
CLIENTS_PER_HOUR=18000 #(Clients per hour, per 1 core of DC)
#2,000,000 clients for 6000 relays
SCALING_CONSTANT = float(2000000/6000)
c_str=0

plt.xlabel('Number of Relays')
plt.ylabel('Percentage of relays with ConsenSGX support')
plt.grid(True)
#plt.xscale('log')
#plt.yscale('log')
plt.title('Percentage of relays with ConsenSGX support required vs number of relays')
ZT_PQ_TIME_np = np.array(ZT_PQ_TIME[50])
params_zt = curve_fit(quadratic_function, N_np, ZT_PQ_TIME_np)

N=[]
Y = []
Y_bw= []
yerror =[]
i = 5000
BW_FOR_ONE_CLIENT_bits=20000*8 #20KB
while(i<=100000):
	TIME_PER_CLIENT=(ZT_PQ_TIME[50][(i/5000)-1])
	err_TIME_PER_CLIENT=(ZT_PQ_STD[50][(i/5000)-1])
	CLIENTS_PER_HOUR=3600*1000/TIME_PER_CLIENT #(3600 * 1000 ms in an hour)
	err_CLIENTS_PER_HOUR=3600*1000/err_TIME_PER_CLIENT

	r_bw = CLIENTS_PER_HOUR * BW_FOR_ONE_CLIENT_bits/ 3600
	Y_bw.append(r_bw)

	Y.append(((i*SCALING_CONSTANT)/CLIENTS_PER_HOUR/i)*100)
	yerror.append(((i*SCALING_CONSTANT)/err_CLIENTS_PER_HOUR/i)*100)
	N.append(i)
	i+=5000

N_np = np.array(N)
Y_np = np.array(Y)
params_curve = curve_fit(quadratic_function, N_np, Y_np)
a,b,c = params_curve[0]
#y_xpir = quadratic_function(x, a, b, c)
x_np = np.arange(min(N),max(N))
y_np = quadratic_function(x_np, a, b, c)


points1 = plt.plot(N, Y, '.', color = str("C")+str(c_ctr))
errbar = plt.errorbar(N, Y, yerror, None,'r',ls='none',mew=4)
print(Y)
print(yerror)
print(Y_bw)
Y_bw_mean = np.mean(Y_bw)/(1000*1000)
Y_bw_mean_str = '%.3f' % Y_bw_mean
line1 = plt.plot(x_np, y_np, '-', color ='g', label='% of ConsenSGX relays (Avg BW required = '+Y_bw_mean_str+' Mbps)')
ax = plt.subplot()
ax.set_ylim(ymin=0)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), shadow=True)
plt.setp(line1, 'linewidth', '2.0')
plt.setp(points1, 'mew', '2.5')

plt.savefig('dc_sgx_req.png', bbox_inches='tight')
plt.close()

######################
# Bandwidth to clients a DC can support
# constants from previous graphs reused
c_str=0

plt.xlabel('Directory cache bandwidth(in Kbps)')
plt.ylabel('Number of clients served(in an hour)')
plt.grid(True)
plt.xscale('log')
plt.title('Number of clients served vs directory cache bandwidth(in Kbps)')
Y = []
yerr =[]
BW_FOR_ONE_CLIENT_bits=20000*8 #20KB
for i in range(1,5001):
	Y.append(i*1000*3600/BW_FOR_ONE_CLIENT_bits)
	

N_np = np.arange(1,5001)
Y_np = np.array(Y)
params_curve = curve_fit(quadratic_function, N_np, Y_np)
a,b,c = params_curve[0]
y_np = quadratic_function(N_np, a, b, c)


line1 = plt.plot(N_np, y_np, '-', color='g', label='Clients served')
#points1 = plt.plot(N_new, Y, POINT_STYLES[c_ctr], label = 'Clients served', color = str("C")+str(c_ctr))
ax = plt.subplot()
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True)
plt.setp(line1, 'linewidth', '2.0')
plt.savefig('dc_bw.png', bbox_inches='tight')
plt.close()

#######
