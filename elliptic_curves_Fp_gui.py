import matplotlib.pyplot as plt
import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox

O = (np.inf, np.inf)

def ec_dis(ec):
    a, b = ec
    discriminant = pow(4*a, 3) + 27 * pow(b, 2)
    if discriminant == 0:
        raise ValueError("Discriminant is 0")

def is_prime(q):
    if q > 1:
        for i in range(2, (q // 2) + 1):
            if (q % i) == 0:
                raise ValueError(f"{q} is not a prime number")
        else:
            return True
    else:
        raise ValueError(f"{q} must be positive integer")

def inv(a, q):
    if a == q:
        raise ValueError("not invertible")
    elif a > q:
        a %= q
        return pow(a, -1, q)
    elif a < q:
        return pow(a, -1, q)
    else:
        raise ValueError("?")


def is_on_curve(ec, q, P):
    a, b = ec
    x, y = P
    if pow(y, 2, q) == pow(x, 3, q) + a*x + b:
        pass
    else:
        raise ValueError

def negative(P):
    x_1, x_2 = P
    return x_1, -x_2

def addition(ec, q, P, Q):
    x_1, y_1 = P
    x_2, y_2 = Q

    a, b = ec

    if x_1 == np.inf and y_1 == np.inf:  # O + P = P
        x_3, y_3 = x_2, y_2

    elif x_2 == np.inf and y_2 == np.inf:  # P + O = P
        x_3, y_3 = x_1, y_1

    elif (x_1 != x_2 and y_1 != y_2) or (x_1 != x_2 and y_1 == y_2):  # point addition
        drv = ((y_2 - y_1) * inv(x_2 - x_1, q)) % q
        x_3 = (pow(drv, 2) - x_1 - x_2) % q
        y_3 = (drv * (x_1 - x_3) - y_1) % q

    elif x_1 == x_2 and y_1 == y_2:  # point doubling
        drv = ((3*pow(x_1, 2) + a)*inv(2*y_1, q)) % q
        x_3 = (pow(drv, 2) - x_1 - x_2) % q
        y_3 = (drv * (x_1 - x_3) - y_1) % q

    elif x_1 == x_2 and (y_1 + y_2) % q == 0:  # point negation
        x_3, y_3 = O

    R = x_3, y_3

    return R

def s_mult(ec, q, k, P):
    result_text = f"Scalar multiplication for {k}{P}:\n"
    R = P
    result_text += f"\t {1} x {P} = {R}\n"
    for i in range(1, k):
        R = addition(ec, q, P, R)
        result_text += f"\t {i + 1} x {P} = {R}\n"
    return result_text

def order(ec, q, P):
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
        x, y = R
        x_subgend.append(x)
        y_subgend.append(y)

    sub_gend_points = x_subgend, y_subgend
    return sub_gend_points

def binary(k):
    binary = bin(k).replace("0b", "")
    binary_arr = [int(bit) for bit in binary]
    return binary_arr

def double(ec, q, P):
    return addition(ec, q, P, P)

def double_and_add(ec, q, k, P):
    n = 1
    R = P
    binary_k = binary(k)[1:]
    steps = []

    steps.append(f"\t First bit is {binary(k)[0]}, we do nothing")
    steps.append(f"\t \t 1 x {P} = {P}\n")

    for bit in binary_k:
        if bit == 0:
            n *= 2
            steps.append(f"\t bit is 0, n= {n}, double")
            steps.append(f"\t \t {n} x {P} = {R}\n")
            R = double(ec, q, R)
        elif bit == 1:
            n = n*2
            R = double(ec, q, R)
            R = addition(ec, q, P, R)
            n += 1
            steps.append(f"\t bit is 1, n= {n}, double and add")
            steps.append(f"\t \t {n} x {P} + {P}= {R}\n")
        else:
            raise ValueError

    return R, steps

def hasse_bound(q):
    hasse_lower = math.floor((-2) * math.sqrt(q) + q + 1)
    hasse_upper = math.floor(2 * math.sqrt(q) + q + 1)
    return hasse_lower, hasse_upper

def graph(ec, q, P):
    n = order(ec, q, P)
    R = O
    x_points = []
    y_points = []
    for _ in range(1, n):
        R = addition(ec, q, P, R)
        x, y = R
        x_points.append(x)
        y_points.append(y)
        if R == O:
            break
    return x_points, y_points

def squareRoot(n, q):
    n = n % q
    if n == 0:
        return n

    for x in range(2, q):
        if ((x * x) % q) == n:
            return x
        else:
            pass

def ec_points(ec, q):
    a, b = ec
    x_points = []
    y_points = []

    for x in range(0, q):
        y_0 = pow(x, 3) + a * x + b % q
        y = squareRoot(y_0, q)

        if y is None:
            pass
        else:
            y = int(y)
            x_points.append(x)
            y_points.append(y)

            if y == 0:
                pass
            else:
                y_inv = -y % q
                x_points.append(x)
                y_points.append(y_inv)

    return x_points, y_points

def display_result(result_text):
    result_window = tk.Toplevel(root)
    result_window.title("Result")
    result_window.geometry("500x400")

    result_frame = ttk.Frame(result_window, padding="10 10 10 10")
    result_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    result_window.columnconfigure(0, weight=1)
    result_window.rowconfigure(0, weight=1)

    canvas = tk.Canvas(result_frame)
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
    scrollable_result_frame = ttk.Frame(canvas)

    scrollable_result_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_result_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    result_label = ttk.Label(scrollable_result_frame, text=result_text, wraplength=400)
    result_label.grid(column=0, row=0, sticky=(tk.W, tk.E))

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    result_frame.grid_columnconfigure(0, weight=1)
    result_frame.grid_rowconfigure(0, weight=1)

def execute_operations():
    try:
        run_operation(None) 
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_operation(event):
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        q = int(entry_q.get())
        ec = (a, b)

        is_prime(q)
        ec_dis(ec)

        result_text = ""

        if var_points.get():
            x_points, y_points = ec_points(ec, q)
            
            result_text = f"Elliptic Curve points and graph: y^2 = x^3 + ({a})x + ({b})\n"
            
            points = list(zip(x_points, y_points))
            order_ec = 0
            for point in points:
                result_text += f"\t{point}\n"
                order_ec += 1
            result_text += f"Order of EC is {order_ec + 1} (including the point at infinity)\n"

            hasse_lower, hasse_upper = hasse_bound(q)
            result_text += f"Hasse bound for {q} is {hasse_lower} <= |E(F_{q})| <= {hasse_upper}\n"
            
            # Plot Elliptic Curve points
            xpoints = np.array(x_points)
            ypoints = np.array(y_points)
            plt.plot(xpoints, ypoints, 'o')
            plt.show()

        if var_addition.get():
            P = (int(entry_x1.get()), int(entry_y1.get()))
            Q = (int(entry_x2.get()), int(entry_y2.get()))
            
            # Perform addition operation

            #is_on_curve(ec, q, P)
            #is_on_curve(ec, q, Q)
            result = addition(ec, q, P, Q)
            result_text = f"{P} + {Q} = {result}\n"

            


        if var_scalar_mult.get():
            k = int(entry_k.get())
            P = (int(entry_x1.get()), int(entry_y1.get()))
            result_text += s_mult(ec, q, k, P)

        if var_double_and_add.get():
            k = int(entry_k.get())
            P = (int(entry_x1.get()), int(entry_y1.get()))
            result, steps = double_and_add(ec, q, k, P)
            steps_text = "\n".join(steps)
            step_count = len(binary(k))
            result_text = f"Total steps: {step_count}\n"
            result_text += f"Result: {result}\n{steps_text}\n"

        if var_order.get():
            P = (int(entry_x1.get()), int(entry_y1.get()))
            order_p = order(ec, q, P)
            x_subgend, y_subgend = sub_gend(ec, q, P)

            result_text += f"Order of {P} is {order_p}\n"
            plt.scatter(x_subgend, y_subgend)
            plt.title(f'Subgroup generated by {P}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()

        display_result(result_text)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def clear_parameters():
    entry_x1.delete(0, tk.END)
    entry_y1.delete(0, tk.END)
    entry_x2.delete(0, tk.END)
    entry_y2.delete(0, tk.END)
    entry_k.delete(0, tk.END)


root = tk.Tk()
root.title("Elliptic Curve Operations")

mainframe = ttk.Frame(root, padding="20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.N, tk.E, tk.S))


#top_frame = ttk.Frame(mainframe)
#top_frame.grid(column=0, row=0, columnspan=1, sticky=(tk.N, tk.E))

input_frame = ttk.Frame(mainframe)
input_frame.grid(column=0, row=1, rowspan=6, sticky=(tk.W, tk.N))


#ttk.Label(top_frame, text="""
#          To construct an elliptic curve over a finite field,
#          please provide the parameters a and b for the equation
#          y^2 = x^3 + ax + b, 
#          along with the prime number p.""", 
#          wraplength=500, justify=tk.CENTER).grid(column=0, row=0, sticky=tk.N)

ttk.Label(input_frame, text="a:").grid(column=0, row=1, sticky=tk.W)
entry_a = ttk.Entry(input_frame, width=7)
entry_a.grid(column=1, row=1, sticky=(tk.W, tk.E))

ttk.Label(input_frame, text="b:").grid(column=0, row=2, sticky=tk.W)
entry_b = ttk.Entry(input_frame, width=6)
entry_b.grid(column=1, row=2, sticky=(tk.W, tk.E))

ttk.Label(input_frame, text="p:").grid(column=0, row=3, sticky=tk.W)
entry_q = ttk.Entry(input_frame, width=7)
entry_q.grid(column=1, row=3, sticky=(tk.W, tk.E))

ttk.Label(input_frame, text="P (x1,y1):").grid(column=0, row=4, sticky=tk.W)
entry_x1 = ttk.Entry(input_frame, width=7)
entry_x1.grid(column=1, row=4, sticky=(tk.W, tk.E))
entry_y1 = ttk.Entry(input_frame, width=7)
entry_y1.grid(column=2, row=4, sticky=(tk.W, tk.E))

ttk.Label(input_frame, text="Q (x2,y2):").grid(column=0, row=5, sticky=tk.W)
entry_x2 = ttk.Entry(input_frame, width=7)
entry_x2.grid(column=1, row=5, sticky=(tk.W, tk.E))
entry_y2 = ttk.Entry(input_frame, width=7)
entry_y2.grid(column=2, row=5, sticky=(tk.W, tk.E))

ttk.Label(input_frame, text="k:").grid(column=0, row=6, sticky=tk.W)
entry_k = ttk.Entry(input_frame, width=7)
entry_k.grid(column=1, row=6, sticky=(tk.W, tk.E))

var_points = tk.BooleanVar()
var_addition = tk.BooleanVar()
var_scalar_mult = tk.BooleanVar()
var_double_and_add = tk.BooleanVar()
var_order = tk.BooleanVar()

ttk.Radiobutton(input_frame, text="Elliptic Curve points and graph", variable=var_points, value=1).grid(column=3, row=2, sticky=tk.W)
ttk.Radiobutton(input_frame, text="Addition", variable=var_points, value=2).grid(column=3, row=3, sticky=tk.W)
ttk.Radiobutton(input_frame, text="Scalar multiplication", variable=var_points, value=3).grid(column=3, row=4, sticky=tk.W)
ttk.Radiobutton(input_frame, text="Scalar multiplication with double and add algorithm", variable=var_points, value=4).grid(column=3, row=5, sticky=tk.W)
ttk.Radiobutton(input_frame, text="Order of an element and its graph", variable=var_points, value=5).grid(column=3, row=6, sticky=tk.W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_rowconfigure(0, weight=1)

button_clear = ttk.Button(mainframe, text="Clear", command=clear_parameters)
button_clear.grid(column=0, row=7, padx=(0, 5), sticky="w")

button_run = ttk.Button(mainframe, text="Run Operations", command=execute_operations)
button_run.grid(column=1, row=7, padx=(5,0), sticky="w")



root.mainloop()
