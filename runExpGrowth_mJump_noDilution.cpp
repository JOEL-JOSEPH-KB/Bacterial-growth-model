#include <iostream>
#include "library_models.cpp"
#include <typeinfo>



int main( int argc, char *argv[] ){


	auto modeltype = Model_simple_ind_omega;
	

	double dt_standard; 
	std::vector<double> omegas;
	std::vector<double> phis;
	std::vector<double> TT_lim;
	std::vector<double> TT_lim1;
	std::vector<double> TT_lim2;
	std::vector<double> TT_lim3;

	const double dilution=0.1; 

	for( int rep=0; rep<1000; rep++){

	std::ofstream file;
			std::vector<std::vector<int>> mJump = {{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0}};

				phis = { 0.3 };
				omegas={ 1.0 };
			


	
	std::cout << "rep = " << rep << "\n";

		struct par p; 
		p.eps = 1e-3; 
		p.g = 0.5; 
        p.n0 = 1.0;
		p.k_T = 10.0; 
		p.k_Q = 1e-9; 
		//p.sigma = 100.0;
        for(int j=0; j<phis.size();j++){ 

            p.phi = phis[j];
        for( int i=0; i<omegas.size(); i++ ){
            p.omega = omegas[i];
		file.open("./numerical_data/Branching_growth/No_dilution_rep_"+std::to_string(rep)+","+std::to_string(dilution)+","+std::to_string(p.phi)+","+std::to_string(p.omega)+","+std::to_string(p.n0)+".txt");//getDTstandard( n_vec, dt_vec,"Standard/DT_standard_Model_ind.txt");



		std::vector<cell> cells_lin;
    	std::vector<int> types_lin; 


        runLineageGrowth_MNR( modeltype, (int)1e4, p, types_lin, cells_lin );
            double dt_lin = 0;
            int n_lin = 0;
            
            for( int k=0; k<cells_lin.size(); ++k){ if(types_lin[k]==0){dt_lin+= cells_lin[k].div-cells_lin[k].born; n_lin++;} }
            
        double t_lim = dt_lin/(double)n_lin;
        

    	double t_lim_1 = 20*t_lim; 
            

		
		std::vector<cell> cells_in;  
		std::vector<std::string> types_in;  


		
		std::vector<cell> cells;
		std::vector<std::string> types;
		runGrowth_MNR_analysis_wTypes( modeltype, t_lim_1, cells_in, false, p, true, cells );

		int n_1 = 0; int n_2 = 0; int n_3 = 0; int n_4 = 0;  
		for( auto c: cells){if(c.cell_type==1){n_1++;};if(c.cell_type==2){n_2++;};if(c.cell_type==3){n_3++;};if(c.cell_type==4){n_4++;}}
		std::cout<<n_1 <<","<<n_2 <<","<<n_3<<","<<n_4  << "\n";



		cells_in = cells; 


		
		n_1 = 0; n_2 = 0; n_3 = 0;n_4 = 0;  
		for( auto c: cells){if(c.cell_type==1){n_1++;};if(c.cell_type==2){n_2++;};if(c.cell_type==3){n_3++;};if(c.cell_type==4){n_4++;}}
	
			 
			runGrowth_MNR_analysis_wTypes( modeltype, 3.1*t_lim, cells_in, false, p, false, cells );
			
			 n_1 = 0; n_2 = 0; n_3 = 0;n_4 = 0;  

		int i_cell, i_mother;

		for(auto c: cells){ i_cell =c.cell_type; i_mother = c.mother_type; mJump[i_mother][i_cell]++;   }


		} // NN
	} // omega
		for( int ii=0; ii<mJump.size(); ii++){
					std::cout << ii << "\n";

					file << mJump[ii][0] << ",";
					for( int jj=1; jj<mJump[ii].size()-1; jj++ ){

						file << mJump[ii][jj]<<",";
					}
					file <<mJump[ii][3]<< "\n";
				}	
	file.close();	
	} // rep

	return 0; 
	
}


