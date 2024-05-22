import matplotlib.pyplot as plt
import numpy as np
import math

O = (np.inf,np.inf)



def ec_dis(ec):
    a,b = ec
    discriminant = pow(4*a,3) + 27 * pow(b,2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")
     

def is_prime(q):
    if q > 1:
        for i in range(2, (q//2)+1):    
            if (q % i) == 0:
                raise ValueError(f"{q} is not a prime number")
        else:
            True
    else:
        raise ValueError(f"{q} must be positive integer")


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
    if pow(y,2,q) == (pow(x,3,q) + a*x + b)%q:
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
        drv = ((3*pow(x_1,2)+a)*inv(2*y_1,q)) %q  
        x_3 = (pow(drv,2) - x_1 - x_2) %q
        y_3 = (drv * (x_1 - x_3) - y_1) %q

    elif x_1 == x_2 and (y_1 + y_2)%q == 0: #point negation
        x_3,y_3 = O

    

    
    R = x_3,y_3

    return R


def s_mult(ec,q, k, P):
    print(f"Scalar multiplication for {k}{P}:")
    R = P
    print(f"\t {1} x {P} = {R}") 
    for i in range(1, k):
        R = addition(ec, q, P, R)
        print(f"\t {i+1} x {P} = {R}")   
        


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
        print(f"\t {i} x {P} = {R}")
        x, y = R
        x_subgend.append(x)
        y_subgend.append(y)

    print(f"\t {sub_order} x {P} = {O}")
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
    
    print(f"\t First bit is {binary(k)[0]}, we do nothing")
    print(f"\t \t 1 x {P} = {P}")
    print("")

    for bit in binary_k:
        if bit == 0:
            n *= 2

            print(f"\t bit is 0, n= {n}, double")

            print(f"\t \t {n} x {P} = {R}")
            R = double(ec,q,R)
            print("")
            
        elif bit == 1:
            n = n*2 
            R = double(ec,q,R) #double
            R = addition(ec,q,P,R) #add
            n += 1

            print(f"\t bit is 1, n= {n}, double and add")

            print(f"\t \t {n} x {P} + {P}= {R}")
            print("")
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

def center_text(message, width=80):
    lines = message.strip().split('\n')
    centered_lines = [line.center(width) for line in lines]    
    centered_message = '\n'.join(centered_lines)
    
    return centered_message

def default_case():
    print("No valid input provided, restarting...")

def main():

    
    print(center_text(("""
To construct an elliptic curve over a finite field, 
please provide the parameters a and b for the equation 
  y^2 = x^3 + ax + b 
along with the prime number p.
               """)))
    
    a = int(input("a: "))
    b = int(input("b: "))
    ec = (a,b)
    q = int(input("q: "))



    is_prime(q)
    ec_dis(ec)

    # a = 12
    # b = 45
    # ec = (a,b)
    # q = 983
    
    



    while True:

        operation = input("""
       Please choose an operation:
    1: Elliptic Curve points and graph
    2: Addition
    3: Scalar multiplication
    4: Scalar multiplication with double and add algorithm
    5: Order of an element and its graph
    0: Exit
       Enter the operation: """)

        if operation.strip() == "":
            print("No input provided, restarting...")
            continue

        match operation:
            case "1": #1: Elliptic Curve points and graph


                x_points, y_points = ec_points(ec,q)

                print(f"Elliptic Curve points and graph: y^2 = x^3 + ({a})x + ({b})")
                print("\t(inf,inf)")
                points = list(zip(x_points, y_points))  
                order_ec = 0
                for point in points:
                    print(f"\t{point}")
                    order_ec += 1
                print(f"Order of EC is {order_ec + 1} (including the point at infinity)")

                hasse_bound(q)

                xpoints = np.array(x_points)
                ypoints = np.array(y_points)

                plt.plot(xpoints, ypoints, 'o')
                plt.title(f"Elliptic Curve: $y^2 = x^3 + {a}x + {b}$ over F_{q}")
                plt.show()



            case "2": #2: Addition
                x_1 , y_1 = input("P: ").split()
                x_2 , y_2 = input("Q: ").split()

                x_1 = int(x_1)
                y_1 = int(y_1)
                x_2 = int(x_2)
                y_2 = int(y_2)

                P = x_1 , y_1
                Q = x_2 , y_2

                print(f"{P} + {Q} = {addition(ec,q,P,Q)}")

                
            case "3": #3: Scalar multiplication
                k = int(input("k:"))

                x_1 , y_1 = input("P: ").split()

                x_1 = int(x_1)
                y_1 = int(y_1)
                
                P = x_1 , y_1
                
                s_mult(ec,q,k,P)


            case "4": #4: Scalar multiplication with double and add algorithm
                k = int(input("k:"))
                
                
                x_1 , y_1 = input("P: ").split()

                x_1 = int(x_1)
                y_1 = int(y_1)
                
                P = x_1 , y_1

                print(f"\t Binary form of k: {binary(k)}")
                
                double_and_add(ec,q,k,P)        

                print(f"""
    Normal scalar multiplication takes {k} steps, 
    but double-and-add algorithm takes {len(binary(k))} steps.""")      

            case "5": # Order of an element and its graph
                x_1 , y_1 = input("P: ").split()

                x_1 = int(x_1)
                y_1 = int(y_1)
                
                P = x_1 , y_1


                print(f"\t Subgroup generated by {P} is: ")
                
                x_subgend , y_subgend = sub_gend(ec,q,P)


                xpoints_gend = np.array(x_subgend)
                ypoints_gend = np.array(y_subgend)

                plt.plot(xpoints_gend, ypoints_gend, 'o')
                plt.show()

                print(f"\t Order of {P} is {order(ec,q,P)}")

            case "0":
                break
            case _:
                default_case()
                




if __name__ == "__main__":
    main()
