import numpy as np 
import os 
import pandas as pd
import copy 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LogNorm, Normalize
import seaborn as sns
from scipy.signal import correlate
import re

def GeoMean( v ): 
	log_v = [np.log(i) for i in v]
	return np.exp(np.sum(log_v)/len(v))

def timeMean( v,dt ): 

	w = [v[i]*dt[i] for i in range(len(v))]

	return np.sum(w)/np.sum(dt)

def dataAnalysis( folder, L, whichTypes_vec ): 

	L = [i for i in L if "DS" not in i]

	N_ID, Q = [],[] 
	N_r_3, N_ID_3, Q_3 = [],[],[]

	N_r, N_r_tm, N_r_max = [],[],[]
	N_m, N_m_tm, N_m_max = [],[],[]
	N_n, N_n_tm, N_n_max = [],[],[]
	N_m_min, N_r_min, N_n_min = [],[],[]

	N_type = []

	N_dt = []

	N_all_m, N_all_r, N_all_n, N_all_s, N_all_dt = [],[],[],[],[]

	N_l = len(L)
	for l in L:
		print(l) 

		D = pd.read_csv( folder + l )

		ID_unique = np.unique( D.ID )
		types = []

		for i, ID in enumerate( ID_unique ):

			types.append(np.unique([str(ii) for ii in D.type[D.ID==ID]])[0])


		for i, ID in enumerate( ID_unique ):
        
			for whichType in whichTypes_vec: 
				if whichType in str(types[i]) and i<len(ID_unique):
			
					N_ID.append( ID )
					Q_r = []
					Q_r_tm = []
					Q_r_max = []
					Q_r_min = []

					Q_m = []
					Q_m_tm = []
					Q_m_max = []
					Q_m_min = []

					Q_n = []
					Q_n_tm = []
					Q_n_max = []
					Q_n_min = []

					Q_type = []

					temp = []

		
					Q_all_m, Q_all_n, Q_all_r, Q_all_s, Q_all_dt  = [],[],[],[],[]

					Q_dt = []

			
					if i<len(ID_unique)-15:
					
						for j in range(-15,15):

							Q_m.append( np.array(D.m[D.ID==ID_unique[i+j]])[0] )
							Q_m_tm.append( timeMean( np.array(D.m[D.ID==ID_unique[i+j]]),np.array(D.dt[D.ID==ID_unique[i+j]])) )
							Q_m_max.append( np.max(np.array(D.m[D.ID==ID_unique[i+j]])) )
							Q_m_min.append( np.min(np.array(D.m[D.ID==ID_unique[i+j]])) )
							
							Q_r.append( np.array(D.r[D.ID==ID_unique[i+j]])[0] )
							Q_r_tm.append( timeMean( np.array(D.r[D.ID==ID_unique[i+j]]),np.array(D.dt[D.ID==ID_unique[i+j]])) )
							Q_r_max.append( np.max(np.array(D.r[D.ID==ID_unique[i+j]])) )
							Q_r_min.append( np.min(np.array(D.r[D.ID==ID_unique[i+j]])) )

							Q_n.append( np.array(D.n[D.ID==ID_unique[i+j]])[0] )
							Q_n_tm.append( timeMean( np.array(D.n[D.ID==ID_unique[i+j]]),np.array(D.dt[D.ID==ID_unique[i+j]])) )
							Q_n_max.append( np.max(np.array(D.n[D.ID==ID_unique[i+j]])) )
							Q_n_min.append( np.min(np.array(D.n[D.ID==ID_unique[i+j]])) )

							Q_type.append( np.array(D.type[D.ID==ID_unique[i+j]])[0])

							Q_all_m.append( np.array(D.m[D.ID==ID_unique[i+j]]) ) 
							Q_all_r.append(  np.array(D.r[D.ID==ID_unique[i+j]]))  
							Q_all_n.append(  np.array(D.n[D.ID==ID_unique[i+j]]))  
							Q_all_s.append(  np.array(D.s[D.ID==ID_unique[i+j]]))  
							Q_all_dt.append(  np.array(D.dt[D.ID==ID_unique[i+j]]))  

							Q_dt.append( np.sum(np.array(D.dt[D.ID==ID_unique[i+j]])) )


						N_r.append( Q_r )
						N_r_tm.append( Q_r_tm )
						N_r_max.append( Q_r_max )
						N_r_min.append( Q_r_min )

						N_m.append( Q_m )
						N_m_tm.append( Q_m_tm )
						N_m_max.append( Q_m_max )
						N_m_min.append( Q_m_min )
						
						N_n.append( Q_n )
						N_n_tm.append( Q_n_tm )
						N_n_max.append( Q_n_max )
						N_n_min.append( Q_n_min )

						N_type.append( Q_type )

						N_all_m.append( Q_all_m )
						N_all_r.append( Q_all_r )
						N_all_n.append( Q_all_n )
						N_all_s.append( Q_all_s )
						N_all_dt.append( Q_all_dt )

						N_dt.append( Q_dt )
	

	return [N_dt, N_r_min, N_n_min, N_m_min,N_r_max, N_n_max, N_m_max,N_r_tm, N_n_tm, N_m_tm, N_r, N_n, N_m, N_all_m, N_all_r, N_all_n, N_all_s, N_all_dt, N_l]
 
 #######################################
 
def dataAnalysis2( vec_in ):


    N_DT, N_r_min, N_n_min, N_m_min,N_r_max, N_n_max, N_m_max,N_r_tm, N_n_tm, N_m_tm, N_r, N_n, N_m, N_all_m, N_all_r, N_all_n, N_all_s, N_all_dt, N_l = vec_in

    N_cells = len(N_r[0])
    N_cells_2 = len(N_r)


    mean_dt_ = [[] for i in range(N_cells)]

    mean_r_ = [[] for i in range(N_cells)]
    mean_r_tm_ = [[] for i in range(N_cells)]
    mean_r_max_ = [[] for i in range(N_cells)]
    mean_r_min_ = [[] for i in range(N_cells)]

    mean_m_ = [[] for i in range(N_cells)]
    mean_m_tm_ = [[] for i in range(N_cells)]
    mean_m_max_ = [[] for i in range(N_cells)]
    mean_m_min_ = [[] for i in range(N_cells)]

    mean_n_ = [[] for i in range(N_cells)]
    mean_n_tm_ = [[] for i in range(N_cells)]
    mean_n_max_ = [[] for i in range(N_cells)]
    mean_n_min_ = [[] for i in range(N_cells)]



    for i in range( len(N_r) ):

        for j in range(N_cells):


            mean_r_[j].append( N_r[i][j] )
            mean_r_tm_[j].append( N_r_tm[i][j] )
            mean_r_max_[j].append( N_r_max[i][j] )
            mean_r_min_[j].append( N_r_min[i][j] )

            mean_m_[j].append( N_m[i][j] )
            mean_m_tm_[j].append( N_m_tm[i][j] )
            mean_m_max_[j].append( N_m_max[i][j] )
            mean_m_min_[j].append( N_m_min[i][j] )

            mean_n_[j].append( N_n[i][j] )
            mean_n_tm_[j].append( N_n_tm[i][j] )
            mean_n_max_[j].append( N_n_max[i][j] )
            mean_n_min_[j].append( N_n_min[i][j] )

            mean_dt_[j].append( N_DT[i][j] )



    mean_dt = [GeoMean(i) for i in mean_dt_]

    mean_r = [np.mean(i) for i in mean_r_]
    std_r = [np.std(i) for i in mean_r_]

    mean_r_tm = [np.mean(i) for i in mean_r_tm_]
    std_r_tm= [np.std(i) for i in mean_r_tm_]

    mean_r_max = [np.mean(i) for i in mean_r_max_]
    std_r_max= [np.std(i) for i in mean_r_max_]

    mean_r_min = [np.mean(i) for i in mean_r_min_]
    std_r_min= [np.std(i) for i in mean_r_min_]

    mean_m = [np.mean(i) for i in mean_m_]
    std_m = [np.std(i) for i in mean_m_]

    mean_m_tm = [np.mean(i) for i in mean_m_tm_]
    std_m_tm= [np.std(i) for i in mean_m_tm_]

    mean_m_max = [np.mean(i) for i in mean_m_max_]
    std_m_max= [np.std(i) for i in mean_m_max_]

    mean_m_min = [np.mean(i) for i in mean_m_min_]
    std_m_min= [np.std(i) for i in mean_m_min_]

    mean_n = [np.mean(i) for i in mean_n_]
    std_n = [np.std(i) for i in mean_n_]

    mean_n_tm = [np.mean(i) for i in mean_n_tm_]
    std_n_tm= [np.std(i) for i in mean_n_tm_]

    mean_n_max = [np.mean(i) for i in mean_n_max_]
    std_n_max= [np.std(i) for i in mean_n_max_]

    mean_n_min = [np.mean(i) for i in mean_n_min_]
    std_n_min= [np.std(i) for i in mean_n_min_]



    mean_r_norm = [i/(mean_r_tm[0]) for i in mean_r_tm]
    mean_n_norm = [i/(mean_n_tm[0]) for i in mean_n_tm]
    mean_m_norm = [i/(mean_m_tm[0]) for i in mean_m_tm]

    return N_cells,N_cells_2,N_l, mean_r_min, mean_m_min, mean_n_min, N_all_r, N_all_m, N_all_n, mean_r_tm, mean_m_tm, mean_n_tm, mean_dt



#######################################


fig = plt.figure(figsize=(6,3),dpi=300)

folders = ["./numerical_data/dormancy_analysis/mDorm/",
"./numerical_data/dormancy_analysis/rDorm/",
"./numerical_data/dormancy_analysis/mrDorm/"]

whichTypes =[["1"],["2"],["3"]]
titles_vec = ["m-dormant","r-dormant","mr-dormant"]

N_sim = [1e4,  1e6, 1e6]
count = 0
letters = ['B','C','D']
for i_f,f in enumerate(folders):

	t = whichTypes[i_f]

	count += 1

	L = os.listdir( f )
	L = [i for i in L if "DS" not in i]

	out = dataAnalysis( f,L,t )
	#print('hejhej')
	#print(f)
	if len(out[0])>0: 
		N_cells,N_cells_2,N_l, mean_r_min, mean_m_min, mean_n_min, N_all_r, N_all_m, N_all_n, mean_r_tm, mean_m_tm, mean_n_tm, mean_dt  = dataAnalysis2(out)


		mean_Q_min = [mean_r_min[i]/(mean_r_min[i]+mean_n_min[i]) for i in range(len(mean_r_min))]
		mean_Q_tm = [mean_r_tm[i]/(mean_r_tm[i]+mean_n_tm[i]) for i in range(len(mean_r_tm))]

		plt.subplot(1,3, count)


			
		numbers = re.findall(r'[0-9]+',L[0])
		plt.title(titles_vec[i_f])

		
		if i_f==0: 
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_r_min, marker='.', label='r', color='red')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_m_min, marker='.', label='m', color='blue')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_n_min, marker='.', label='n', color='green')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_dt, marker='.', label=r'$\Delta$t', color='orange')

		else: 
	
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_r_min, marker='.',  color='red')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_m_min, marker='.', color='blue')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_n_min, marker='.',  color='green')
			plt.plot(np.arange(-15,N_cells-15)[:],	mean_dt, marker='.', color='orange')



		plt.xlabel("Cell number in lineage")	
		plt.ylabel('(Time weighted) mean')
		plt.yscale('symlog')
		ax = plt.gca()
		ax.text(-0.2,1.05,letters[i_f],fontsize=20,transform=ax.transAxes) 


fig.legend( ncol=4, loc=10,bbox_to_anchor=(0.55, 0.06))
	
fig.tight_layout(pad=2.5)
plt.savefig( "Figure_5B.png" )

plt.show()	
