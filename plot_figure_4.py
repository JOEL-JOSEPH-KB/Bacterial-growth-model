import numpy as np 
import os 
import pandas as pd
import copy 
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
import seaborn as sns


def heatPlotPrepare( folder, L_in ): 

	L = [i for i in L_in if "DS" not in i]


	D = pd.read_csv( folder + L[0] )
	omega_vec = np.unique( D.omega )
	phi_vec = np.unique( D.phi )


	dict_temp = [0 for i in range(len(phi_vec))]
	phi_dict = [dict(zip(phi_vec, dict_temp)) for i in range(len(omega_vec))]


	NP_dict_0 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) ) 
	NP_dict_1 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	NP_dict_2 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	NP_dict_3 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	NP_dict_33 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	NP_dict_23 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	NP_dict_10 = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	
	GR_dict = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )

	M_dict = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	N_dict = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )
	R_dict = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )

	Denom = copy.deepcopy( dict(zip(omega_vec, phi_dict)) )

	content = []


	count = 0



	for l in L:

		D = pd.read_csv( folder + l )

		for i in range(len(D)): 
	

			if not np.isnan(D.t0[i]): 
				NP_dict_0[D.omega[i]][D.phi[i]] += D.t0[i]
			if not np.isnan(D.t1[i]):  
				NP_dict_1[D.omega[i]][D.phi[i]] += D.t1[i]  
			if not np.isnan(D.t2[i]): 
				NP_dict_2[D.omega[i]][D.phi[i]] += D.t2[i] 
			if not np.isnan(D.t3[i]): 
				NP_dict_3[D.omega[i]][D.phi[i]] += D.t3[i] 

			
			nom1 = 0
			nom2 = 0
			nom3 = 0
			denom = 0
		


			denom += D.t0[i]

			denom += D.t1[i]
			nom1 += D.t1[i]
	
			denom += D.t2[i]
			nom2 += D.t2[i]
		
			denom += D.t3[i]
			nom3 += D.t3[i]
				
			NP_dict_2[D.omega[i]][D.phi[i]] += nom2
			NP_dict_1[D.omega[i]][D.phi[i]] += nom1
			NP_dict_3[D.omega[i]][D.phi[i]] += nom3

			Denom[D.omega[i]][D.phi[i]] += denom

			M_dict[D.omega[i]][D.phi[i]] += D.m[i]
			R_dict[D.omega[i]][D.phi[i]] += D.r[i]
			N_dict[D.omega[i]][D.phi[i]] += D.n[i]

			GR_dict[D.omega[i]][D.phi[i]] += np.log(2)/D.dt_mean[i]

	


			content.append( [np.log(2)/D.dt_mean[i],D.m[i],D.r[i],D.n[i]])

		


	heat_0 = np.zeros((len(omega_vec), len(phi_vec)))
	heat_2 = np.zeros((len(omega_vec), len(phi_vec)))
	heat_1 = np.zeros((len(omega_vec), len(phi_vec)))
	heat_3 = np.zeros((len(omega_vec), len(phi_vec)))

	heat_M = np.zeros((len(omega_vec), len(phi_vec)))
	heat_R = np.zeros((len(omega_vec), len(phi_vec)))
	heat_N = np.zeros((len(omega_vec), len(phi_vec)))
	heat_GR = np.zeros((len(omega_vec), len(phi_vec)))




	for i,omega in enumerate(omega_vec): 
		for j,phi in enumerate(phi_vec):

			denom = Denom[omega][phi]

			heat_0[i][j] = NP_dict_0[omega][phi]/denom
			heat_2[i][j] = NP_dict_2[omega][phi]/denom
			heat_1[i][j] = NP_dict_1[omega][phi]/denom
			heat_3[i][j] = NP_dict_3[omega][phi]/denom

			heat_M[i][j] = M_dict[omega][phi]/len(L)
			heat_R[i][j] = R_dict[omega][phi]/len(L)
			heat_N[i][j] = N_dict[omega][phi]/len(L)

			heat_GR[i][j] = GR_dict[omega][phi]/len(L)

	return heat_1, heat_2,heat_3, omega_vec, phi_vec, heat_M, heat_R, heat_N, heat_GR, content		



folder_BP = "numerical_data/parameter_sweep_phi_vs_omega/"
L_BP = os.listdir( folder_BP )


H_BP_1, H_BP_2,H_BP_3, phi_vec, omega_vec, heat_M, heat_R, heat_N, heat_GR,content = heatPlotPrepare( folder_BP,L_BP )


log_norm = LogNorm(vmin=1e-9, vmax=1)



fig = plt.figure(figsize=(12, 6), constrained_layout=True)
spec = fig.add_gridspec(ncols=4, nrows=4)


ax4 = fig.add_subplot(spec[0:2, 0])
ax5 = fig.add_subplot(spec[0:2, 1])
ax6 = fig.add_subplot(spec[0:2, 2])
ax1 = fig.add_subplot(spec[2:4, 0])
ax2 = fig.add_subplot(spec[2:4, 1])
ax3 = fig.add_subplot(spec[2:4, 2])
ax7 = fig.add_subplot(spec[1:3, 3])


ax4.text(0,1.05,'A',fontsize=20,transform=ax4.transAxes)
ax5.text(0,1.05,'B',fontsize=20,transform=ax5.transAxes)
ax6.text(0,1.05,'C',fontsize=20,transform=ax6.transAxes)
ax1.text(0,1.05,'D',fontsize=20,transform=ax1.transAxes)
ax2.text(0,1.05,'E',fontsize=20,transform=ax2.transAxes)
ax3.text(0,1.05,'F',fontsize=20,transform=ax3.transAxes)
ax7.text(0,1.05,'G',fontsize=20,transform=ax7.transAxes)



s6 =sns.heatmap(heat_N.T,cmap='rainbow',xticklabels=phi_vec,yticklabels=omega_vec, ax=ax6)
s5 =sns.heatmap(heat_R.T,cmap='rainbow',xticklabels=phi_vec,yticklabels=omega_vec, ax=ax5)
s4 =sns.heatmap(heat_M.T,cmap='rainbow',xticklabels=phi_vec,yticklabels=omega_vec, ax=ax4)

s1 = sns.heatmap(H_BP_1.T,cmap='crest', norm=log_norm,xticklabels=phi_vec,yticklabels=omega_vec, ax=ax1)
s2 = sns.heatmap(H_BP_2.T,cmap='crest', norm=log_norm,xticklabels=phi_vec,yticklabels=omega_vec, ax=ax2)
s3 = sns.heatmap(H_BP_3.T,cmap='crest', norm=log_norm,xticklabels=phi_vec,yticklabels=omega_vec, ax=ax3)

s7 =sns.heatmap(heat_GR.T,cmap='Oranges',xticklabels=phi_vec,yticklabels=omega_vec, ax=ax7)


s1.set_title('m-dormant', fontsize=14)
s2.set_title('r-dormant', fontsize=14)
s3.set_title('mr-dormant', fontsize=14)
s7.set_title('Growth rate', fontsize=14)
s4.set_title('m', fontsize=17)
s5.set_title('r', fontsize=17)
s6.set_title('n', fontsize=17)


s1.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s2.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s3.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s4.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s5.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s6.set(ylabel=r'$\phi$', xlabel=r'$\omega$')
s7.set(ylabel=r'$\phi$', xlabel=r'$\omega$')



plt.savefig('figures/figure_4.png')
plt.show()








