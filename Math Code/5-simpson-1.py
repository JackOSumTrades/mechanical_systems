def f(x):
    return x**4 - 2*x + 1

N = 10
a = 0.0
b = 2.0
h = (b-a)/N

s1 = 0.0 # sum for odds

for k in range(1,N,2):
    s1 += f(a+k*h)

s2 = 0.0

for k in range(2,N,2):
    s2 += f(a+k*h)
    
I = h/3 * (f(a) + f(b) + 4 * s1 + 2 * s2)

print(I)
