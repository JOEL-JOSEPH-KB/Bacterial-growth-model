import numpy as np 
import os 
import pandas as pd
import copy 
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LogNorm, Normalize
import seaborn as sns



folder_branch = "numerical_data/Branching_growth/"
folder_lin = "numerical_data/Lineage_growth/"

FF = [folder_lin, folder_branch]
titles = ["Lineage","Branching"]

QQ = []
NN = []


for f in FF: 
	Q = []
	N = 0

	folder = f

	L = os.listdir( folder )

	L = [i for i in L if "DS" not in i]

	DD = np.zeros((4,4))
	for l in L: 

		D = np.loadtxt( folder + l, delimiter=',' )


		Q.append( [np.sum(D[ii])/np.sum(D) for ii in range(len(D))]	)

		 
		N+= np.sum(D)

	QQ.append(Q)	

	NN.append(N)
	
I = []		
l_dat = []		
count = 1
Ym,Ys = [],[]
for ij_q, Q in enumerate(QQ):
	dat = [[] for i in range(4)] 
	for q in Q: 
		for i_q,e_q in enumerate(q):
			dat[i_q].append( e_q )
	l_dat.append(dat)		 
	count += 1
	y_m = [np.mean(i) for i in dat]
	y_s = [np.std(i)/np.sqrt(len(dat[0])-1) for i in dat]

	for i in range(len(y_m)): 
		if y_m[i]==0: 
			y_m[i] = 1/NN[ij_q]
			I.append((ij_q,i))

	Ym.append( y_m )
	Ys.append( y_s )

plt.figure(figsize=(3,3),dpi=300)

X = [[0,0.5,1.0,1.5], [0.2,0.7,1.2,1.7]]

for i in range(len(Ym)): 
	plt.bar(X[i], Ym[i], yerr=Ys[i], align='center', alpha=0.5, width=0.2, ecolor='black', capsize=10)
	if i ==1: 
		plt.bar([1.2,1.7], Ym[i][2:], alpha=0.5,width=0.2, fc='none', hatch='///' )		

	
		


X_pos = [i+0.1 for i in X[0]]
labels = [r'$\emptyset$','m','r','mr']
plt.xticks(X_pos, labels)
ax = plt.gca()
ax.text(-0.2,1.05,'A',fontsize=20,transform=ax.transAxes) 


plt.yscale('log')
plt.ylabel('Probability')
plt.xlabel('Dormancy type')
plt.legend(['Lineage','Branch'])


plt.tight_layout()

plt.savefig("figures/Figure5_1.png")


plt.show()	


