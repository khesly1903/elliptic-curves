import matplotlib.pyplot as plt
import numpy as np
import math
import random
O = (np.inf,np.inf)

def ec_dis(a,b):
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     

def ec_point():
    pass

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
    print(f"ORDER OF {P}")
    R = P
    order_of_point = 1
    while True:
        R = addition(ec, q, P, R)
        order_of_point += 1
        if R == O:
            break
    return order_of_point


def hasse_bound(q):
    hasse_lower = (-2)*math.sqrt(q)+q+1
    hasse_upper = 2*math.sqrt(q)+q+1
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





def main():
    ec = -7,10
    q=13
    P=11,4
    Q=3,4
    W=11,4 #order18

    print()
    print(f"ADDITION OF {P} AND {Q}:")
    print(f"{P} + {Q} = {addition(ec,q,P,Q)}")
    print()

    s_mult(ec,q,19,P)
    print()

    print(order(ec,q,P))

    print()

 
    

    x,y = graph(ec,q,P) 
    xpoints = np.array(x)
    ypoints = np.array(y)

    plt.plot(xpoints, ypoints, 'o')
    plt.show()


    
if __name__ == "__main__":
    main()
    

