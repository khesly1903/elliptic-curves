import matplotlib.pyplot as plt
import numpy as np
import math

O = (np.inf,np.inf)

def ec_dis(ec):
    a,b = ec
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     

def is_prime(p):
    if p > 1:
        for i in range(2, (p//2)+1):    
            if (p % i) == 0:
                raise ValueError(f"{p} is not a prime number")
        else:
            True
    else:
        raise ValueError(f"{p} must be positive integer")


def inv(a,q):
    if a == q:
        raise ValueError("not invertible")
    elif a > q:
        a %= q
        return pow(a,-1,q)
    elif a < q:
        return pow(a,-1,q)
    else:
        raise ValueError("??nasi")
    

def is_on_curve(ec,q,P):
    a,b = ec
    x,y = P
    if pow(y,2,q) == pow(x,3,q) + a*x + b:
        pass
    else:
        raise ValueError

def negative(P):
    x_1,x_2 = P
    return x_1,-x_2

def addition(ec,q,P,Q):

    x_1,y_1 = P
    x_2,y_2 = Q

    a,b = ec
    
    if x_1 == np.inf and y_1 == np.inf: # O + P = P
        x_3,y_3 = x_2,y_2 

    elif x_2 == np.inf and y_2 == np.inf: # P + O = P
        x_3,y_3 = x_1,y_1
    
    elif (x_1 != x_2 and y_1 != y_2) or (x_1 != x_2 and y_1 == y_2): #point addition
        drv = ((y_2 - y_1) * inv(x_2-x_1,q)) %q
        x_3 = (pow(drv,2) - x_1 - x_2) %q
        y_3 = (drv * (x_1 - x_3) - y_1) %q

    elif x_1 == x_2 and y_1 == y_2: #point doubling
        drv = ((3*pow(x_1,2)+a)*(pow(2*y_1,-1,q))) %q
        x_3 = (pow(drv,2) - x_1 - x_2) %q
        y_3 = (drv * (x_1 - x_3) - y_1) %q

    elif x_1 == x_2 and (y_1 + y_2)%q == 0: #point negation
        x_3,y_3 = O

    

    
    R = x_3,y_3

    return R


def s_mult(ec,q, k, P):
    print(f"SCALAR MULTIPLICATION {k}{P}:")
    R = P
    print(f"{1} x {P} = {R}") 
    for i in range(1, k):
        R = addition(ec, q, P, R)
        print(f"{i+1} x {P} = {R}")   
        
    return R

def order(ec,q,P):
    R = P
    order_of_point = 1
    while True:
        R = addition(ec, q, P, R)
        order_of_point += 1
        if R == O:
            break
    return order_of_point


def sub_gend(ec, q, P):

    R = O
    sub_order = order(ec, q, P)  
    x_subgend = []
    y_subgend = []

    for i in range(1, sub_order):  
        R = addition(ec, q, P, R)  
        print(f"{i} x {P} = {R}")
        x, y = R
        x_subgend.append(x)
        y_subgend.append(y)

    print(f"{sub_order} x {P} = {O}")
    sub_gend_points = x_subgend, y_subgend  
    
    return sub_gend_points  

def binary(k):
    binary = bin(k).replace("0b","") 
    binary_arr = []
    for bit in binary:
        bit = int(bit) #conver to int cz in str form
        binary_arr.append(bit)

    return binary_arr
        

def double(ec,q,P):
    return addition(ec,q,P,P)

def double_and_add(ec,q,k,P):
    n = 1
    R = P

    
    binary_k = binary(k)[1:] #no operation for first bit
    
    print(f"-----First bit is {binary(k)[0]}, we do nothing")
    print(f"1 x {P} = {P}")

    for bit in binary_k:
        if bit == 0:
            n *= 2
            print("--")
            print(f"----bit is 0, n= {n}, double")
            print("--")
            print(f"{n} x {P} = {R}")
            R = double(ec,q,R)
            
        elif bit == 1:
            n = n*2 
            R = double(ec,q,R) #double
            R = addition(ec,q,P,R) #add
            n += 1
            print("--")
            print(f"----bit is 1, n= {n}, double and add")
            print("--")
            print(f"{n} x {P} + {P}= {R}")
        else:
            raise(ValueError)

    return R

def hasse_bound(q):
    hasse_lower = math.floor((-2)*math.sqrt(q)+q+1)
    hasse_upper = math.floor(2*math.sqrt(q)+q+1)
    print(f"Hasse bound for {q} is {hasse_lower} <= #E <= {hasse_upper}")

def graph(ec,q,P):
    n=order(ec,q,P)
    R = O
    x_points = []
    y_points = []
    for _ in range(1,n):
        R = addition(ec, q, P, R)
        x,y = R
        x_points.append(x)
        y_points.append(y)
        if R == O:
            break
    return x_points,y_points




def squareRoot(n, q): 
    n = n % q
    if n == 0: #to catch when y=0, bcs otw return none
        return n
    
    for x in range (2, q):
        if ((x * x) % q == n) :
            return x
        else:
            pass


def ec_points(ec,q):
    a,b = ec
    x_points = []
    y_points = []

    for x in range(0,q):
        y_0 = pow(x,3) + a*x + b % q # y^2 = x^3 + ax + b but y_0 is y^2

        y = squareRoot(y_0,q)
        
        
        if y == None: #y can be None
            pass
        else: # check y is int or not  & #find the under part
            y = int(y)
            P = x,y
            #if is_on_curve(ec,q,P) == True:
            x_points.append(x)
            y_points.append(y)

            if y == 0: # find the upper part
                pass #there is no point
            else:
                y_inv = -y % q
                x_points.append(x)
                y_points.append(y_inv)

    return x_points,y_points




def main():
    pass
    
if __name__ == "__main__":
    main()
    

