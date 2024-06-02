

#include <iostream>
#include "library_models.cpp"


int main( int argc, char *argv[] ){
	
	
	auto modeltype = Model_simple_ind_omega_full;
	

	double dt_standard; 
	std::vector<double> omegas;
	std::vector<double> phis;

    


	for( int rep=0; rep<1000; rep++){

	std::ofstream file;

	file.open("numerical_data/parameter_sweep_phi_vs_omega/Rep_"+std::to_string(rep)+".txt");

	phis = { 0.1,0.2, 0.3, 0.4, 0.5, 0.6,0.7,0.8 };
	omegas={0.1,0.2,0.5,1.0,2.0,5.0,10.0};
			
	
	file <<"Rep,phi,omega,dt_mean,n_cells,n,m,r,s,t0,t1,t2,t3\n";
	std::cout << "rep = " << rep << "\n";

	struct par p; 
	p.eps = 1e-3; 
	p.g = 0.5; 
    p.n0 = 1.0;
	p.k_T = 10.0; 
	p.k_Q = 1e-9; 

    for(int j=0; j<phis.size();j++){ 
        p.phi = phis[j];
    for( int i=0; i<omegas.size(); i++ ){
        p.omega = omegas[i];

  

		std::vector<cell> cells_lin;
    	std::vector<int> types_lin; 




		std::vector<cell_full> cells;
		std::vector<int> types;
		double empty_phase = 0; 

		int N_cells = (int) 1e4;
            


		runLineageGrowth_MNR_full( modeltype, N_cells, p, types, cells, empty_phase );
	
        double DDT = 0;
        int cd = 0;
       
        
       
        double n_c = cells.size();

            

        double n_mean = 0;double m_mean = 0; double r_mean = 0; double s_mean = 0;
        double dt_mean = 0; 
        int counter = 0;  
            for( auto c: cells){ 
            	counter++; 
            	double dt_tot_sc = 0; 	
            	
            	double n_mean_sc= 0;double m_mean_sc = 0; double r_mean_sc = 0; double s_mean_sc = 0;
            	
            	for( auto d: c.content ){

            		n_mean_sc += d[2]*d[6]; m_mean_sc+= d[0]*d[6]; r_mean_sc += d[1]*d[6]; s_mean_sc += d[3]*d[6];
            		dt_tot_sc += d[6];


            	}

            	n_mean += n_mean_sc/(dt_tot_sc*n_c); 
            	m_mean += m_mean_sc/(dt_tot_sc*n_c); 
            	r_mean += r_mean_sc/(dt_tot_sc*n_c); 
            	s_mean += s_mean_sc/(dt_tot_sc*n_c); 

            	dt_mean += dt_tot_sc/n_c;
                
             
            	}
			
            double t0 = 0; double t1 = 0; double t2 = 0; double t3 = 0; 

			for( int ii = 0; ii<types.size(); ii++){

				switch( types[ii] ){

					case 0: t0++; break; 
					case 1: t1++; break; 
					case 2: t2++; break; 
					case 3: t3++; break; 



				}


			}
            

		file << rep<<","<< p.phi <<","<<p.omega<<","<<dt_mean<<","<<cells.size()<<","<<n_mean<<","<<m_mean<<","<<r_mean<<","<<s_mean << ","
		<< t0 << "," << t1 << "," << t2 << "," << t3 <<"\n";



		} // NN
	} // omega
	file.close();	
	} // rep

	return 0; 
	
}


