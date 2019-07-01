import sys
import base64
import os.path
import hashlib
import numpy as np
import matplotlib.pyplot as plt

CONSENSUS_MAIN='2018_09/'
CONSENSUS_2018_FOLDER='consensuses-2018-09/'
SERVER_DESCRIPTORS_FOLDER='server_descriptors/'

TARGET_HIST_CONSENSUS=CONSENSUS_MAIN+CONSENSUS_2018_FOLDER+'25/2018-09-25-00-00-00-consensus'

SERVER_DESCRIPTORS_FOLDERS_BYMONTH = ['2018_09/server-descriptors-2018-09/','2018_08/server-descriptors-2018-08/','2018_07/server-descriptors-2018-07/','2018_06/server-descriptors-2018-06/','2018_05/server-descriptors-2018-05/','2018_04/server-descriptors-2018-04/','2018_03/server-descriptors-2018-03/']

no_of_routers_in_2018 = 0
no_of_descriptors_matched = 0
no_of_descriptors_not_matched = 0
null_policies_ctr = 0
null_family_ctr = 0

Policies=[]
Policies_hash=[]
Family_hash=[]
Policies_size=[]
Family=[]
Family_size=[]

hash_set = set()
size_list = []
policy_set = set()

family_hash_set = set()
family_size_list=[]
family_set = set()

Descriptor_sizes = []
Descriptor_sizes_pruned = []
with open(TARGET_HIST_CONSENSUS,"r") as consensus2018:
	for line in consensus2018:
		line = line.strip()
		words = line.split(' ')
		if(words[0]=='r'):
			no_of_routers_in_2018=no_of_routers_in_2018+1
			b64_router1_desc_hash=words[3]
			router_name=words[1]
			#print(b64_router1_desc_hash)
			rem = len(b64_router1_desc_hash)%4
			pad_length = 0
			if(rem!=0):				
				pad_length = 4 - rem
			for i in range(pad_length):
				b64_router1_desc_hash=b64_router1_desc_hash+'='
			print("Router's name: " + router_name)			
			print("Router's b64 hash: " + b64_router1_desc_hash)
			router1_filename=base64.b64decode(b64_router1_desc_hash).encode('hex')
			print("Router's filename(Hex): " +router1_filename)
	
			router1_desc_file_found = True;
			policy1=""
			family1=""
			ROUTER1_FILENAME = ""
			ROUTER1_FOUND = False 
		
			for k in range(len(SERVER_DESCRIPTORS_FOLDERS_BYMONTH)):
				ROUTER1_FILENAME=SERVER_DESCRIPTORS_FOLDERS_BYMONTH[k]+str(router1_filename[0])+'/'+str(router1_filename[1])+'/'+router1_filename					
				if(os.path.isfile(ROUTER1_FILENAME)):
					ROUTER1_FOUND = True
					desc_size = os.path.getsize(ROUTER1_FILENAME)
					Descriptor_sizes.append(desc_size)
					no_of_descriptors_matched+=1
					break

			
			if(ROUTER1_FOUND):
				desc_size = os.path.getsize(ROUTER1_FILENAME)
				with open(ROUTER1_FILENAME,"r") as relay_descriptor1:
					for line in relay_descriptor1:
						words = line.split()
						if(words[0]=="accept" or words[0]=="reject"):
							policy1=policy1+'\n'+line
						if(words[0]=="family"):
							family1=family1+'\n'+line
			
				if(policy1==""):
					null_policy_ctr+=1
				if(family1==""):
					null_family_ctr+=1
				#Policies.append(policy1)
				#Policies_size.append(len(policy1))
				#sha256 = hashlib.sha256()
				#sha256.update(policy1)
				#Policies_hash.append(sha256.digest())
				#Family.append(family1)
				sub_size = len(policy1) + len(family1)				
				desc_size_pruned = desc_size - (len(policy1) + len(family1))				
				Descriptor_sizes_pruned.append(desc_size_pruned)	

				#sha256v2 = hashlib.sha256()
				#sha256v2.update(family1)
				#Family_hash.append(sha256v2.digest())
				#remove repeated hashes and sizes from the result lists
				#Compute unique policy size

			else:
				no_of_descriptors_not_matched+=1				
						
print("No of relays matched to their descriptors = "+str(no_of_descriptors_matched))
print("No of relays whose descriptors were not found = "+str(no_of_descriptors_not_matched))

Descriptor_sizes.sort()
limit = 2000
count_in_bucket=[]
current = 0
for i in Descriptor_sizes:
	if(i<=limit):
		current+=1
	else:
		count_in_bucket.append(current)
		limit+=2000
		current=1
count_in_bucket.append(current)
n=np.arange(1,len(count_in_bucket)+1)
ycoords = [str(x * 2000) for x in n]
plt.xticks(n, ycoords)
plt.bar(n,count_in_bucket, width=-0.9, align='edge')

# Make some labels.
labels = ["%d" % i for i in count_in_bucket]

ax = plt.subplot()
for i in np.arange(0,len(count_in_bucket)):
    height = count_in_bucket[i]
    ax.text( i + (0.55), height + 5, labels[i], ha='center', va='bottom')

plt.grid(True)
plt.title('Histogram of relay descriptor sizes')
plt.ylabel('Number of relays')
plt.xlabel('Size of relay descriptors (in bytes)')
plt.savefig('hist_relays.png')
plt.close()



count_in_bucket=[]
current = 0
limit = 1000
Descriptor_sizes_pruned.sort()
print(Descriptor_sizes_pruned)
for i in Descriptor_sizes_pruned:
	if(i<=limit):
		current+=1
	else:
		count_in_bucket.append(current)
		limit+=200
		current=1
count_in_bucket.append(current)

n=np.arange(1,len(count_in_bucket)+1)
ycoords = [str(1000 + ((x-1) * 200)) for x in n]
plt.xticks(n, ycoords)
print(len(Descriptor_sizes_pruned))
print(count_in_bucket)
plt.bar(n,count_in_bucket, width=-0.9, align='edge')
labels = ["%d" % i for i in count_in_bucket]

ax = plt.subplot()
for i in np.arange(0,len(count_in_bucket)):
    height = count_in_bucket[i]
    ax.text( i + (0.55), height + 5, labels[i], ha='center', va='bottom')

plt.grid(True)
plt.title('Histogram of relay descriptor sizes after pruning family and exit policies')
plt.ylabel('Number of relays')
plt.xlabel('Size of relay descriptors (in bytes)')
plt.savefig('hist_relays_pruned.png')
plt.close()
		
		
	


#print("Null policies = " + str(null_policies_ctr))
#print("Null Family = " + str(null_family_ctr))

#Sort Policies_size zipped to Policies_hash by Policies_hash
#Z = sorted(zip(Policies_hash,Policies_size,Policies))
#sorted_policies_hash, sorted_policies_size = zip(*Z)
'''
repeated_policies = 0
for l in Z:
	if(l[0] not in hash_set):
		hash_set.add(l[0])
		size_list.append(l[1])
		policy_set.add(l[2])
	else:
		repeated_policies+=1

Y = sorted(zip(Family_hash, Family))
for l in Y:
	if(l[0] not in family_hash_set):
		family_hash_set.add(l[0])
		family_size_list.append(len(l[1]))
		family_set.add(l[1])

print("Number of repeated policies = "+str(repeated_policies))
print("Number of unique policies = "+str(len(size_list)))
print("Unique policies size = " + str(sum(size_list)) )

print("Number of unique families = "+str(len(family_hash_set)))
print("Unique families size = " + str(sum(family_size_list)) )

with open("policies","w") as policy_file:
	policy_file.writelines(["%s\n\n" % item for item in policy_set])

with open("families","w") as family_file:
	family_file.writelines(["%s\n\n" % item for item in family_set])
'''

