import numpy as np
import math

O = (np.inf,np.inf)

def ec_dis(a,b):
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     

def ec_point():
    pass

def is_on_curve(ec,q,P):
    a,b = ec
    x,y = P
    if pow(y,2,q) == pow(x,3,q) + a*x + b:
        pass
    else:
        raise ValueError

def ec_addition(ec,q,P,Q):
    x_1,y_1 = P
    x_2,y_2 = Q

    a,b = ec
    
    if x_1 != x_2 and y_1 != y_2: #point addition
        drv = ((y_2 - y_1) * pow(x_2 - x_1,-1,q)) %q
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


def scalar_mult(a, b, k, P):
    R = P
    for i in range(1, k):
        R = ec_addition(a, b, P, R)
    return R


def hasse_bound(q):
    hasse_lower = (-2)*math.sqrt(q)+q+1
    hasse_upper = 2*math.sqrt(q)+q+1
    print(f"Hasse bound for {q} is {hasse_lower} <= #E <= {hasse_upper}")


def main():
    ec = -7,10

    print(ec_addition(ec,13,(5,3),(5,3)))
    print(scalar_mult(ec,13,3,(5,3)))



if __name__ == "__main__":
    main()
    

