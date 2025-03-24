import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt

folder = "./numerical_data/mean_behavior/"
if not os.path.exists(folder):
	os.makedirs(folder)
L = os.listdir( folder )
L = [i for i in L if 'DS' not in i]

D = pd.read_csv( folder + L[0])

n0_vec = np.unique(D.n0)

S_mean,R_mean,M_mean,N_mean,GR,DT = [],[],[],[],[],[]

for n0 in n0_vec: 
	N_mean.append( np.mean(D.n_tm[D.n0==n0]) )
	R_mean.append( np.mean(D.r_tm[D.n0==n0]) )
	S_mean.append( np.mean(D.s_tm[D.n0==n0]) )
	M_mean.append( np.mean(D.m_tm[D.n0==n0]) )
	GR.append(np.mean( [np.log(2)/i for i in D.dt[D.n0==n0]] ))
	DT.append(np.mean( [i for i in D.dt[D.n0==n0]] ) )

cellSize = [R_mean[i]+S_mean[i]+M_mean[i] for i in range(len(R_mean))]
cellSize_woR = [S_mean[i]+M_mean[i]+0.5*R_mean[i] for i in range(len(R_mean))]
plt.figure(dpi=300, figsize=(8,3))
plt.subplot(1,2,2)

plt.scatter(GR,R_mean,marker='o', label='r', alpha=0.5, ec='black')
plt.scatter(GR,cellSize,marker='o', label='cell size', alpha=0.5, ec='black')

plt.yscale('log')
plt.legend()
plt.xlabel(r'GR')
plt.ylabel('Mean content number per cell')
plt.tight_layout()
plt.subplot(1,2,1)
plt.scatter(n0_vec,GR,marker='o', alpha=0.5,color='magenta', ec='black')
plt.xlabel(r'$n_0$')
plt.ylabel(r'GR ')
plt.tight_layout()

if not os.path.exists('./figures'):
	os.makedirs('./figures')
plt.savefig('./figures/GrowthLaw_.png')


plt.figure(dpi=300, figsize=(8,3))

plt.subplot(1,2,2)
plt.scatter(GR,R_mean,marker='o', label='r', alpha=0.5, ec='black')
plt.scatter(GR,cellSize,marker='o', label='cell size', alpha=0.5, ec='black')
plt.yscale('log')
plt.legend()
plt.xlabel(r'GR')
plt.ylabel('Mean content number per cell')
plt.tight_layout()
plt.subplot(1,2,1)
plt.scatter(n0_vec,np.array(GR),marker='o', alpha=0.5,color='magenta', ec='black')
plt.xlabel(r'$n_0$')
plt.ylabel(r'GR')
plt.tight_layout()

if not os.path.exists('./figures/main_figures'):
	os.makedirs('./figures/main_figures')
plt.savefig('./figures/main_figures/figure_2_growth_law.png')

plt.figure(dpi=300, figsize=(3,3))
plt.scatter(GR,[R_mean[i]/cellSize_woR[i] for i in range(len(R_mean))],marker='o', label='r', alpha=0.5, ec='black')
plt.yscale('log')
plt.legend()
plt.xlabel(r'GR')
plt.ylabel('Mean content number per cell')
plt.tight_layout()
plt.savefig('./figures/ratio_law.png')
plt.show()



