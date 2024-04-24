import numpy as np

O = (np.inf,np.inf)

def ec(a,b):
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     

def ec_point():
    pass


def ec_addition(a,P,Q):
    x_1,y_1 = P
    x_2,y_2 = Q
    
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

def main():
    a = 2
    print(ec_addition(a,(2,3),(4,-4)))


if __name__ == "__main__":
    main()
    

