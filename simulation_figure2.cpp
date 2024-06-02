
#include <iostream>
#include "library_models.cpp"
#include <iomanip>      // std::setprecision


int main(){

std::ofstream file;

std::vector<double> n0_vec = {0.01, 0.02, 0.05,0.1,0.2, 0.5, 1.0, 2.0, 5.0,10, 20.0, 50.0, 100.0, 200.0, 500.0}; 

for( int rep=0; rep<100; rep++){
file.open("numerical_data/mean_behavior/Rep_"+std::to_string(rep)+".txt"); 
file <<"n0,m_tm,r_tm,n_tm,s_tm,dt\n";

for( auto n0: n0_vec){

	auto modeltype = Model_simple_ind_omega_full; 

	struct par p; 
	p.eps = 1e-3; 
	p.g = 0.5; 
	p.n0 = 1.0;
	p.k_T = 10.0; 
	p.k_Q = 1e-9; 
	p.n0 = n0; 
	p.n_stored = n0;
	p.phi = 0.5; 
	p.omega = 1.0; 

	std::vector<cell_full> cells_lin;
    std::vector<int> types_lin;

    runLineageGrowth_MNR_full( modeltype, (int)2e3, p, types_lin, cells_lin,0 );

    for( auto c: cells_lin){

    	double r_tm = 0; double n_tm = 0; double m_tm = 0; double s_tm = 0;
    	double dt = 0;  

    	for( auto d: c.content){

    		m_tm += d[0]*d[6];
    		r_tm += d[1]*d[6];
    		n_tm += d[2]*d[6];
    		s_tm += d[3]*d[6];
    		dt += d[6];
    		
    	}
    	file <<n0<<","<<m_tm/dt<<","<<r_tm/dt<<","<<n_tm/dt<<","<<s_tm/dt<<","<<dt<<"\n";
    }
}
} // for rep
return 0; 
} // main
