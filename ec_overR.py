import numpy as np
import math
import matplotlib.pyplot as plt

O = (np.inf,np.inf)

def disc(ec):
    a,b = ec
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     
def is_on_curve(ec,P):
    a,b = ec
    x,y = P
    if P == O:
        return True
    elif y == math.sqrt(pow(x,3) + a*x + b):
        return True
    elif y == -math.sqrt(pow(x,3) + a*x + b):
        return True
    else:
        raise ValueError(f"{P} is not on curve")



def addition(ec,P,Q):
    a,b = ec
    x_1,y_1 = P
    x_2,y_2 = Q

    is_on_curve(ec,P)
    is_on_curve(ec,Q)

    if x_1 != x_2 and y_1 != y_2: #point addition
        drv = (y_2 - y_1) / (x_2 - x_1)
        x_3 = pow(drv,2) - x_1 - x_2
        y_3 = drv * (x_1 - x_3) - y_1

    elif x_1 == x_2 and y_1 == y_2: #point doubling
        drv = (3*pow(x_1,2) + a) / (2*y_1)
        x_3 = pow(drv,2) - x_1 - x_2
        y_3 = drv * (x_1 - x_3) - y_1

    elif x_1 == x_2 and y_1 == -y_2: #point negation
        x_3,y_3 = O


    R = x_3,y_3

    return R

def sc_mult(ec,q,k,P):
    is_on_curve(ec,P)

    R = P
    print(f"{1} x {P} = {R}") 
    for i in range(1, k):
        R = addition(ec, q, P, R)
        print(f"{i+1} x {P} = {R}") 
    
    is_on_curve(ec,R) #in any case :D
    return R


def plot_elliptic_curve(ec):
    a,b = ec
    x = np.linspace(-10, 10, 400)
    y_squared = x**3 + a * x + b

    plt.figure(figsize=(8, 6))
    
    plt.plot(x, np.sqrt(y_squared), 'b', label="Positive Root")
    plt.plot(x, -np.sqrt(y_squared), 'b', label="Negative Root")
    
    plt.title(f"Elliptic Curve: $y^2 = x^3 + {a}x + {b}$")
    
    plt.xlabel("x")
    plt.ylabel("y")
    
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    
    plt.show()

def main():
    a = int(input("a: "))
    b = int(input("b: "))
    ec = (a,b)
    
    #ec = (-7,10)
    # P = (5,10)
    # Q = (-1,4)
    
    
    #ec = (-12,4)
    
    plot_elliptic_curve(ec)

    disc(ec)
    print("For addition, write two points ")
    x_0 , y_0 = input("P: ").split()
    x_1 , y_1 = input("Q: ").split()

    x_0 = int(x_0)
    y_0 = int(y_0)
    x_1 = int(x_1)
    y_1 = int(y_1)

    P = x_0 , y_0
    Q = x_1 , y_1
    
    is_on_curve(ec,P)
    is_on_curve(ec,Q)

    print(f"{P} + {Q} = {addition(ec,P,Q)}")

if __name__ == "__main__":
    main()
    

