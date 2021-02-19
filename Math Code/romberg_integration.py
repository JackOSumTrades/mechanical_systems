 
def romberg_recurs():
    pass
    R_i_m_plus = R_i_m+(1/(4^m-1))*(R_i_m-R_i_m_minus)
    
    
def integrate_trapezoid(func, integ_from, integ_to, n_iter):
    h = (integ_to-integ_from)/n_iter
    
    s = 0.5*func(integ_from) + 0.5*func(integ_to)
    
    for k in range(1,n_iter):
        s += func(integ_from+k*h)
    
    return h*s
        
        
def integrate_romberg_trap():

    f = lambda x: x**4 - 2*x + 1
    integ_from = 0
    integ_to = 2
    
    
    R_1_1 = 0
    R_2_1 = integrate_trapezoid(f, integ_from, integ_to, 10)
    
    R_2_2 = R_2_1+(1/(4^2-1))*(R_2_1-R_1_1)
    
    print(R_1_1)
    print(R_2_1) 
    return R_2_2
	
    
print(integrate_romberg_trap())