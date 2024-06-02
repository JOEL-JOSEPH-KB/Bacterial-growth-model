#include <iostream>
#include <random>
#include <fstream>
#include <map>
#include <string>
#include <sstream>


class cell{ 
public: 

	double n, r, s, m,p, x, y, born, div; 
	int ID, mother_ID, cell_type, mother_type; 

	cell( double n_in, double r_in, double s_in, double m_in, double p_in, double x_in, double y_in, double born_in, double div_in, int ID_in=0, int cellType_in=0, int mother_ID_in=0, int mother_type_in =0 ){

		n = n_in;
		r = r_in;
		s = s_in;
		m = m_in;
		p = p_in;
		x = x_in;
		y = y_in;

		born = born_in;
		div = div_in;

		ID = ID_in; 
		cell_type = cellType_in;
		mother_ID = mother_ID_in; 
		mother_type = mother_type_in; 
	}
};

class cell_full{ 
public: 

	double n, r, s, m,p, x, y, born, div; 
	int ID, mother_ID, cell_type, mother_type; 

	std::vector<std::vector<double>> content;

	cell_full( double n_in, double r_in, double s_in, double m_in, double born_in, double div_in, std::vector<std::vector<double>> content_in,  int ID_in=0, int cellType_in=0, int mother_ID_in=0, int mother_type_in =0  ){

		n = n_in;
		r = r_in;
		s = s_in;
		m = m_in;

		born = born_in;
		div = div_in;

		ID = ID_in; 
		cell_type = cellType_in;
		mother_ID = mother_ID_in; 
		mother_type = mother_type_in;
		content = content_in;  
	}
};

struct par {

	double g; 
	double K;
	double n0; 
	double eps; 
	double n_stored;
	double phi;
	double sigma;  
	double k_n;
	double omega;
	double k_m; 
	double k_T; 
	double k_Q;
};


void randPart( double c_in, double &c_out_1, double &c_out_2 ){

	std::random_device rd;
	std::mt19937 mt(rd());
	std::uniform_int_distribution<> dist(0, 1);

	if(dist(mt)==1){ 
		c_out_1 = std::floor( c_in/2 );
		c_out_2 = std::ceil( c_in/2 );
	}
	else{ 
		c_out_1 = std::ceil( c_in/2 );
		c_out_2 = std::floor( c_in/2 );
	}
}

void division_wID_full( cell_full c, cell_full &c1, cell_full &c2, double t, double dt, int &n_ID, struct par p, double phase ){

	double n1,n2,r1,r2,s1,s2,m1,m2;

	double born = t;

	int mother_type = c.cell_type; 
	int mother_ID = c.ID; 
	int cell_type = 0;
    
	randPart( c.n, n1, n2 );
	randPart( c.r, r1, r2 );
	randPart( c.s, s1, s2 );
	randPart( c.m, m1, m2 );
    
    

	std::vector<std::vector<double>> content1; content1.push_back({m1,r1,n1,s1,p.n0,0,dt, phase}); 
	std::vector<std::vector<double>> content2; content2.push_back({m2,r2,n2,s2,p.n0,0,dt, phase});

	c1 = cell_full( n1,r1,s1,m1, born, 0, content1, n_ID, cell_type, mother_ID, mother_type );	
	c2 = cell_full( n2,r2,s2,m2, born, 0, content2, n_ID+1, cell_type,  mother_ID, mother_type );

	n_ID += 2; 
}

void cellDivision_MNR_full( cell_full &c_old, cell_full &c_new, cell_full modeltype( cell_full, double&, double, double, struct par p), double t_in, struct par p, int &typeDetection, double phase ){

	double t = t_in;

	std::random_device rd;
	std::mt19937 mt(rd());
	std::uniform_real_distribution<double> dist(0.0, 1.0);

	double rn1, rn2; 
	double dt; 

	std::vector<std::vector<double>> content1 = {};
	std::vector<std::vector<double>> content2 = {};

	cell_full c1(0,0,0,0,0,0, content1);
	cell_full c2(0,0,0,0,0,0, content2);

	int count = 0; 
	
	bool cat1 = false; 
	bool cat2 = false; 
	bool cat3 = false; 

	typeDetection = 0; 

	cell_full c = c_old;

	while(true){	

		if( not cat1 and not cat3 and c.n==0 and c.m==0 ){typeDetection = 1; cat1 = true;}
		if( not cat2 and not cat3 and c.r==0 ){typeDetection = 2; cat2 = true; }
		if( not cat3 and c.m==0 and c.r==0 ){typeDetection = 3; cat3 = true; }



		int empty_ID = -1; 

		count++; 
		rn1 = dist(mt); 
		rn2 = dist(mt); 
		c_old = c; 
		c = modeltype( c, dt, rn1, rn2, p );
		t+=dt; 
		c.content.push_back( {c_old.m,c_old.r,c_old.n,c_old.s,p.n0,t,dt,phase} );
        

		if( c.s>=10 ){


			division_wID_full(c,c1,c2,t,dt,empty_ID,p,phase);


			c1.born = t_in;
			c1.div = t;

			c_new = c1;
            c.born = t_in;
            c_old.div = t;
			c_old.born = t_in;
       
			break;


		} 
	}
} 



void runLineageGrowth_MNR_full( cell_full modeltype( cell_full, double&, double, double, struct par p), int N, struct par p, std::vector<int> &types, std::vector<cell_full> &cells_out, double phase ){

	std::vector<std::vector<double>> content={};
	std::vector<std::vector<double>> content_old={};
	std::vector<std::vector<double>> content_1={};

	cell_full c(10,10,10,10,0,0, content); 
	cell_full c_old(10,10,10,10,0,0, content_old); 
	cell_full c_new(10,10,10,10,0,0, content_1); 
	double t = 0; 
	int typeDetection; 


	for( int i=0; i<N; i++){
            cellDivision_MNR_full(c_old, c_new,  modeltype, t, p, typeDetection, phase );
        
			if(i>1000){

                cells_out.push_back(c_old);
				types.push_back(typeDetection);

			}
			c_old = c_new; 
	} //i-loop			

} // runLineageGrowth
