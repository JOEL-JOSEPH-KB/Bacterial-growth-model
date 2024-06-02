#include <iostream>
#include "library_models.cpp"
#include <iomanip>      // std::setprecision



int main(){

auto modeltype = Model_simple_ind_omega;

std::vector<double> phi_vec = {0.1,0.3, 0.6}; 

struct par p; 
p.sigma = 100.0; 
p.k_Q = 1e-9; 
p.n0 = 1.0;	
p.k_T = 10.0;
p.n_stored = 1.0; 
p.phi = 0.7;
p.omega = 0.5;
p.eps = 1e-3; 

int N_lin = (int)1e6; 

std::ofstream file; 


 


double phase = 0; 
for( int rep=0; rep<100; ++rep){

	file.open("numerical_data/interdivision_time_analysis_figure_3/Dist_rep_"+std::to_string(rep)+".txt"); 
	file << "rep,phi,type,dt\n";

for( auto phi_i: phi_vec){

	std::cout << "phi=" <<phi_i << "\n";

	std::vector<int> types_lin; 
	std::vector<cell> cells_lin; 

	std::vector<int> n_types={0,0,0,0};

	p.phi = phi_i; 

	//runLineageGrowth_MNR( modeltype, N_lin, p, types_lin, cells_lin );
	runLineageGrowth_MNR( modeltype, N_lin, p, types_lin, cells_lin );

	for( int i=0; i<cells_lin.size(); ++i){

		file << rep <<","<<p.phi<<","<<types_lin[i]<<","<<cells_lin[i].div-cells_lin[i].born<<"\n";
	}


}
file.close();
} // rep 


return 0; 
} // main