#include <iostream>
#include "library_models.cpp"
#include <iomanip>      // std::setprecision






int main( int argc, char *argv[] ){

	struct par p; 

	std::vector<double> phi_vec;
	std::vector<double> n_vec;
	std::vector<double> omega_vec;

	std::string Analysis; 

	//Analysis = "r_dormant"; omega_vec = {0.5}; n_vec = {1.0}; phi_vec = {0.4};
	Analysis = "r_dormant"; omega_vec = {1.0}; n_vec = {1.0}; phi_vec = {0.3};
	//Analysis = "m_dormant"; omega_vec = {1.0}; n_vec = {1.0}; phi_vec = {0.5};
	//Analysis = 'mr_dormant';omega_vec = {0.5}; n_vec = {1.0}; phi_vec = {0.4};



	std::ofstream file, file2, file3;




	double n_model = 1; 
	auto modeltype = Model_simple_ind_omega;
	
	double t1,t2; 
	std::vector<cell> cells1,cells2,cells3; 
	

	double T_DS = 10; 

	//std::cout << "start1"<<"\n";

	double dt_standard; 

	std::vector<double> NN;
	std::vector<double> OO;
	p.g = 0.5; 
	


	p.k_T = 10.0; 
	p.k_Q = 1e-9; 

	

		for( int rep=0; rep<100; rep++){

			
		std::cout << "rep = " << rep << "\n";



			
				int i = 0; 


				int N = (int)1e7; 
				
				p.phi = phi_vec[i];
				p.n0 = n_vec[i];	
			 	p.omega = omega_vec[i];
				p.eps = 1e-3; 

			

				bool withLim = false; 
				bool init = true; 
				std::vector<cell> cells_BD; 
				std::vector<std::string> types; 
				std::vector<std::vector<int>> mJump = {{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0}}; 

				runLineageGrowth_MNR_jumpMatrix( modeltype, N,p, mJump );

				file.open("./numerical_data/Lineage_growth/Rep_"+std::to_string(rep)+"_n0="+std::to_string(n_vec[0])+"_omega="+std::to_string(omega_vec[0])+"_phi="+std::to_string(phi_vec[0])+".txt"); 



				for( int ii=0; ii<mJump.size(); ii++){
					std::cout << ii << "\n";

					file << mJump[ii][0] << ",";
					for( int jj=1; jj<mJump[ii].size()-1; jj++ ){

						file << mJump[ii][jj]<<",";
					}
					file <<mJump[ii][3]<< "\n";
				}		
				
				
			
		file.close(); 	
		} // rep loop

	return 0; 
	

}


