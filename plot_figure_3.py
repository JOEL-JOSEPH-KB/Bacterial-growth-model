import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt
import copy

folder = "numerical_data/interdivision_time_analysis_figure_3/"
L = os.listdir( folder )
L = [i for i in L if 'DS' not in i][:2]

temp = [[] for i in range(7)]
D = [copy.deepcopy(temp) for i in range(3)]

Dat = pd.read_csv( folder + L[0])
phi_vec = np.unique(Dat.phi)


for l in L: 
	for i,phi in enumerate(phi_vec): 
	
		Dat = pd.read_csv( folder + l)
		D_sub = Dat.dt[ Dat.phi==phi ]



		D[i][0] = np.concatenate((D[i][0], D_sub[Dat.type==0].to_numpy()))
		D[i][1] = np.concatenate((D[i][1], D_sub[Dat.type==1].to_numpy()))
		D[i][2] = np.concatenate((D[i][2], D_sub[Dat.type==2].to_numpy()))
		D[i][3] = np.concatenate((D[i][3], D_sub[Dat.type==3].to_numpy()))
		D[i][4] = np.concatenate((D[i][4], D_sub[Dat.type==4].to_numpy()))
		D[i][5] = np.concatenate((D[i][5], D_sub[Dat.type==5].to_numpy()))
		D[i][6] = np.concatenate((D[i][6], D_sub[Dat.type==6].to_numpy()))

fig = plt.figure(dpi=300,figsize=(8,3))

labels=[r"$\phi=0.1$",r"$\phi=0.3$",r"$\phi=0.6$"]

letters = ['A','B','C']

for i,D_sub in enumerate(D):
	
	b_min, b_max = 1e9,0

	for j in range(6):
		if len(D_sub[j])>0: 
			b_min = np.min(( b_min, np.min(D_sub[j]) )) 
			b_max = np.max(( b_max, np.max(D_sub[j]) )) 

			print(b_min,b_max)
	bins = np.logspace(np.log10(b_min),np.log10(b_max),50)



	out = [[] for i in range(7)]

	plt.subplot(1,3,i+1)
	#if i>0: 
	plt.title(labels[i])
	
	out[0] = np.histogram(D_sub[0], bins = bins)[0]
	out[1] = np.histogram(D_sub[1], bins = bins)[0]
	out[2] = np.histogram(D_sub[2], bins = bins)[0]
	out[3] = np.histogram(D_sub[3], bins = bins)[0]
	out[4] = np.histogram(D_sub[4], bins = bins)[0]
	out[5] = np.histogram(D_sub[5], bins = bins)[0]
	out[6] = np.histogram(D_sub[6], bins = bins)[0]

	X = []
	for j in range(len(bins)-1): 

		X.append( np.sqrt(bins[j+1]*bins[j]) )	


	norm = 0
	for j in range(len(out)):
		for k in range(len(out[j])):

			norm += out[j][k]*X[k]


	out_norm = np.zeros((len(out),len(out[0])))



	for j in range(len(out)):
		for k in range(len(out[j])):

			out_norm[j][k] = out[j][k]/norm		

	for j in range(len(out)):

		plt.bar(X,out_norm[j],width=np.diff(bins)*0.9905, alpha=0.4)
		plt.xscale('log')

	#print(np.sum(out_norm))
	plt.tight_layout()
	

	plt.yscale('log')
	plt.xscale('log')
	plt.xlabel('Doubling time')
	plt.ylabel('Frequency')

	ax = plt.gca()

	ax.text(0,1.05,letters[i],fontsize=20,transform=ax.transAxes)

plt.tight_layout()

labels = [r'$\emptyset$', 'M','R','MR']
fig.subplots_adjust(bottom=0.25)
fig.legend(labels,loc='upper center',ncol=4, bbox_to_anchor=(0.5,0.1), borderaxespad=0)


plt.savefig('figures/figure3.png')
plt.show()




