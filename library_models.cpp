#include "library_simulation.cpp"



cell Model_simple_ind_omega( cell c, double &dt,double rn1,double rn2, struct par p ){

    double eps = p.eps;

    double Q = c.r/(c.n+c.r+p.k_Q);
    double T = c.n*c.r/((c.n+c.r+p.k_T));


    double rate1,rate2,rate3,rate4;



    rate1 = eps + p.n0*c.m;
    rate2 = 1e-6*c.n + p.omega*(1-Q)*T;
    rate3 = (1-p.phi)*Q*T;
    rate4 = p.phi*Q*T;


    double R = rate1+rate2+rate3+rate4;

    dt = -std::log( rn2 )/R;



    if(rn1<(rate1)/R){
        c.n++;
    }
    else if(rn1<(rate1+rate2)/R){
        c.n--;
        c.r++;
    }
    else if(rn1<(rate1+rate2+rate3)/R){
        c.n--;
        c.s++;
    }
    else if(rn1<(rate1+rate2+rate3+rate4)/R){
        c.n--;
        c.m++;
    }

    return c;
}



cell_full Model_simple_ind_omega_full( cell_full c, double &dt,double rn1,double rn2, struct par p ){

    double Q = c.r/(c.n+c.r+p.k_Q);
    double T = c.n*c.r/((c.n+c.r+p.k_T));
    double rate1,rate2,rate3,rate4;

    rate1 = p.eps + p.n0*c.m;
    rate2 = 1e-6*c.n + p.omega*(1-Q)*T;
    rate3 = (1-p.phi)*Q*T;
    rate4 = p.phi*Q*T;

    double R = rate1+rate2+rate3+rate4;

    dt = -std::log( rn2 )/R;

    if(rn1<(rate1)/R){
        c.n++;
       
    }
    else if(rn1<(rate1+rate2)/R){
        c.n--;
        c.r++;
      
    }
    else if(rn1<(rate1+rate2+rate3)/R){
        c.n--;
        c.s++;
  
    }
    else if(rn1<(rate1+rate2+rate3+rate4)/R){
        c.n--;
        c.m++;
   
    }

    return c;
}


