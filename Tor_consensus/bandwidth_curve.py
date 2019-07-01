import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

def quadratic_function(x, a, b, c):
    return a*x*x + b*x + c

def linear_function(x, a, b):
    return a*x + b

def exponential_function(x, a, b):
    return (x**a)*b

def func(x, a, b):
    return 1.0/(1.0+np.exp(-b*(x-a)))

TARGET_CONSENSUS='2018-06-01-consensus'
consensus = open(TARGET_CONSENSUS,'r')


bw_list = []
for line in consensus:
	words = line.split()
	if(words[0]=='w'):
		subwords = words[1].split('=')
		#BW in KBytes
		bw = subwords[1]
		bw_list.append(int(bw))



bw_list_pruned = []
bw_log_list_pruned = []
for i in bw_list:
	#sum_lns+=(math.log1p(i))
	if(i>100):
		bw_list_pruned.append(i)
		bw_log_list_pruned.append(math.log1p(int(i)))
		#bw_log_list_pruned.append(float(math.log1p(int(i))/ math.log1p(int(2))))

bw_list_pruned.sort()
bw_list_bins=[]
relay_no_bins=[]
bin_ub = 200
current_bin_list = []
current_relay_no_list =[]


for i in bw_list_pruned:
	if(i<=bin_ub):
		current_bin_list.append(i)
		current_relay_no_list.append(i)
	else:
		bw_list_bins.append(float(sum(current_bin_list)/len(current_bin_list)))
		relay_no_bins.append(sum(current_relay_no_list)/len(current_relay_no_list))
		bin_ub=bin_ub+10000
		current_bin_list=[]
		current_relay_no_list=[]
		current_bin_list.append(i)
		current_relay_no_list.append(i)
bw_list_bins.append(float(sum(current_bin_list)/len(current_bin_list)))
relay_no_bins.append(sum(current_relay_no_list)/len(current_relay_no_list))

bin_ub=1000
ctr=1
bw_scaled=[]
'''
for i in bw_list_pruned:
	if(i<=bin_ub):
		bw_scaled.append(i/(bin_ub/10)
	else:
		bw_scaled.append(ctr*10	
'''
#print(relay_no_bins)
#print(bw_list_bins)

bw_list_pruned.sort(reverse=True)
bw_list_exp_pruned=[math.log(x) for x in bw_list_pruned]

relays_np = np.arange(1,len(bw_list_pruned)+1)
params_line = curve_fit(linear_function, relays_np, bw_list_exp_pruned)
#params_line = curve_fit(exponential_function, relay_no_bins, bw_list_bins, p0=[2000., 0.005])

a,b = params_line[0]
print(a,b)
y_line = linear_function(relays_np, a, b)
y_line_new = [math.exp(x) for x in y_line]
#print(y_line)

#a,b, = params_line[0]
y_line = linear_function(relays_np, a, b)
#y_line_new = [math.exp(x) for x in y_line] 

#points1 = plt.plot(relays_np, bw_log_list_pruned, '-', color ='g', label = 'Actual distribution')
#approx_line= plt.plot(relays_np, y_line, '--', color='b', label='Approximated line')

print(len(bw_list_pruned))
points1 = plt.plot(relays_np, bw_list_pruned,'-', color ='g', label = 'Actual distribution')
approx_line= plt.plot(relays_np, y_line_new, '--', color='b', label='Approximated line')
#approx_line= plt.plot([1, 5233],[100000,100], '--', color='b', label='Approximated line')

ax = plt.subplot()
plt.ylim(100,100000)
plt.xlim(0,5233)
ax.legend(loc='upper right')
plt.setp(points1, 'mew', '2.0')
plt.setp(approx_line, 'mew', '2.0')
plt.setp(approx_line, 'linewidth', '2.0')
plt.setp(points1, 'linewidth', '2.0')


#plt.savefig('relay_bws.png', bbox_inches='tight')
plt.grid(True)
#plt.ylabel('log(bandwidth) with bandwidth in KBps')
#plt.xlabel('Number of relays with bandwidth > 2^y KBps')
plt.xlabel('Relay number')
plt.ylabel('Relay bandwidth (in KBps)')
plt.yscale('log')
plt.title('Distribution of relay bandwidths')
plt.savefig('relay_bws.png')
plt.close()


bw_list_size = len(bw_list)
current = 0
curr_count=0

bw_points_list =[]
pr_list=[]

for i in bw_list:
	if (i==current):
		curr_count+=1
		
	if (i!=current):
		if(current!=0):
			bw_points_list.append(current)
			pr_list.append(float(curr_count)/float(bw_list_size))
		curr_count+=1
		current=i
	

plt.grid(True)
plt.ylabel('Bandwidth (in KBps) of relays')
plt.xlabel('Cumulative fraction of relays with > x KBps')
#plt.xscale('log')
#plt.yscale('log')

x_np = np.arange(1,len(bw_list)+1)
points2 = plt.plot(x_np, bw_list, '.', color ='g')
plt.setp(points2, 'mew', '2.0')
ax = plt.subplot()
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), shadow=True)
plt.savefig('pr_relays.png')
plt.close()

		

