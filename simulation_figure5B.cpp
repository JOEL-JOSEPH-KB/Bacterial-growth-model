#include <iostream>
#include "library_models.cpp"
#include <iomanip>


int main( int argc, char *argv[] ){

	struct par p; 

	int N; 

	std::vector<double> phi_vec;
	std::vector<double> n_vec;
	std::vector<double> omega_vec;

	std::vector<std::string> analysis_list ={"r_dormant", "mr_dormant", "m_dormant"}; 

	omega_vec = {1.0}; n_vec = {1.0}; phi_vec = {0.3}; 
	
	for(auto Analysis: analysis_list){ // Loop through all persister types
	
	if( Analysis == "r_dormant" ){ N = (int)1e6;} // cell divisions per lineage
	if( Analysis == "mr_dormant" ){  N = (int)1e6;}
	if( Analysis == "m_dormant" ){  N = (int)1e4;}
	
	std::ofstream file, file2, file3;

	double n_model = 1; 
	auto modeltype = Model_simple_ind_omega;
	
	double t1,t2; 
	std::vector<cell> cells1,cells2,cells3; 
	
	double T_DS = 10;

	double dt_standard; 

	std::vector<double> NN;
	std::vector<double> OO;
	p.g = 0.5; 
	
	p.k_T = 10.0; 
	p.k_Q = 1e-9; 
	

		for( int rep=0; rep<2; rep++){ // number of lineages to analyse

		if( Analysis=="r_dormant"){
			file.open("./numerical_data/dormancy_analysis/rDorm/rep_"+std::to_string(rep)+"_n0="+std::to_string(n_vec[0])+"_omega="+std::to_string(omega_vec[0])+"_phi="+std::to_string(phi_vec[0])+"_N="+std::to_string(N) + ".txt"); 
		}	
		if( Analysis=="m_dormant"){
			file.open("./numerical_data/dormancy_analysis/mDorm/rep_"+std::to_string(rep)+"_n0="+std::to_string(n_vec[0])+"_omega="+std::to_string(omega_vec[0])+"_phi="+std::to_string(phi_vec[0])+"_N="+std::to_string(N) +".txt"); 
		}
		if( Analysis=="mr_dormant"){
			file.open("./numerical_data/dormancy_analysis/mrDorm/rep_"+std::to_string(rep)+"_n0="+std::to_string(n_vec[0])+"_omega="+std::to_string(omega_vec[0])+"_phi="+std::to_string(phi_vec[0])+"_N="+std::to_string(N) +".txt"); 
		}
            
		std::cout << "rep = " << rep << "\n";

			double t1,t2; 

			for( int i=0; i<n_vec.size(); i++ ){

				p.phi = phi_vec[i];
				p.n0 = n_vec[i];
			 	p.omega = omega_vec[i];
				p.eps = 1e-3; 

				bool withLim = false; 
				bool init = true; 
				std::vector<cell> cells_BD; 
				std::vector<std::string> types; 
				std::vector<std::vector<std::vector<double>>> means; 

				runLineageGrowth_MNR_persisterAnalysis( modeltype, N,p, types, means, cells_BD );

				std::string target; 

				int n_BD = cells_BD.size();

				std::string target2="2"; 
				std::string target1="1"; 
				std::string target3="3"; 

				int n_per = 0; 
				

				file <<"NR,type,ID,r,n,m,s,dt\n";
				
				for( int j=20; j<cells_BD.size()-20; j++){

					std::size_t found1 = types[j].find(target1);
					std::size_t found2 = types[j].find(target2);
					std::size_t found3 = types[j].find(target3);

					
					
					if( (Analysis=="r_dormant" and (found2!=std::string::npos and not(found3!=std::string::npos))) or (Analysis=="m_dormant" and (found1!=std::string::npos or found3!=std::string::npos)) or (Analysis=="mr_dormant" and (found3!=std::string::npos)) ){   
					
						n_per++; 
		

						for( int j_sub=j-20; j_sub<j+20; j_sub++){ // loop over 20 cells before target type

							for( auto content_vec: means[ j_sub ]){

								file <<n_per <<"," << types[j_sub] <<"," <<j_sub;

								for( auto var_content: content_vec){

									file <<","<< var_content;

									}
								file << "\n";	
								}
							}

						}

						
				}

			} // n_vec loop
		file.close(); 	
		} // rep loop


	} // analysis_loop
	return 0; 
	

}


