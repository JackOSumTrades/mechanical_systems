from math import sin,pi
import warnings

def integrate_trapezoid(funct, integ_from, integ_to, n_iter):
    pass


def integrate_simpsons(func, integ_from, integ_to, n_iter):
    # func is a mathematical function with one parameter
    # integ_from is the beginning of the integration inteval
    # integ_to is the end of the integration interval
    # n_iter is the number of steps
    
    if n_iter %2 != 0:
        raise ValueError("Number of iterations must be even")
        
    step_h = (integ_to-integ_from)/n_iter
    
    odd_sum = 0.0
    even_sum = 0.0
    
    for i in range(1,n_iter):
        try:
            if i%2==0:
                even_sum += func(integ_from+i*step_h)
            else:
                odd_sum += func(integ_from+i*step_h)
        except ZeroDivisionError:
            
            warnings.warn("Division by zero detected, continuing")
            continue
    estimate = step_h/3 * (func(integ_from) + func(integ_to) + 4*odd_sum + 2*even_sum)
    
    return estimate
    
def demo():
    f = lambda x: sin(x)/x 
    print(integrate_simpsons(f, -pi, pi, 100))
    print(integrate_simpsons(f, 0.000001, pi, 101))
    
demo()