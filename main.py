from decimal import DivisionByZero
import re
import matplotlib.pyplot as plt
import operator as op
import numpy as np


def print_line():
    print("--------------------------------")


def print_help():
    print_line()
    print("Command list:\n"
          "0 0 -- add point (input two numbers separated by spaces);\n"
          "d -- delete all points;\n"
          "v -- view the entered points;\n"
          "c -- calculate the polynomial;\n"
          "h -- display this message;\n"
          "q -- quit")
    print_line()


def print_err():
    print("Incorrect command. To see the list of commands, type \"h\".")

# multiplies polynomial by ax + b, takes the polynomial coefs and (a, b)
def compute_multi(arr, pair):
    if len(arr) == 0:                               # if empty:
        return [pair[0], pair[1]]                   #   return ax+b

    multi1 = [a * pair[0] for a in arr] + [0]       # multiplies poly by ax
    multi2 = [0] + [a * pair[1] for a in arr]       # multiplies poly by b
    
    return list(map(op.add, multi1, multi2))        # adds two together

# builds the basis polynomial, takes the list of points and i
def generate_basis_poly(lst, i):
    ret = []                                        # coef array
    xi = lst[i][0]
    for j in [x for x in range(0, len(lst)) if x != i]:
        xj = lst[j][0]
        ret = compute_multi(ret, (1/(xi-xj), -xj/(xi-xj)))
    return ret

# basis polynomial sum, takes the list of points
def generate_polynomial(lst):
    ret = generate_basis_poly(lst, 0)               # gen the polynomial
    ret = [a * lst[0][1] for a in ret]              # multiply the first basis polynomial
    for i in range(1, len(lst)):

        newarr = generate_basis_poly(lst, i)        # gen the polynomial
        newarr = [a * lst[i][1] for a in newarr]    # multiply the basis polynomial
        ret = list(map(op.add, ret, newarr))        # adds the basis polynomial to the result

    return ret


def frm(num):
    return "{:.4f}".format(num)


def polynom_to_str(pol):
    ret = "y ="
    for i in range(0, len(pol)):
        if pol[i] >= 0:
            ret += " + "
        else:
            ret += " - "
        ret += frm(abs(pol[i]))
        if i < len(pol)-1:
            ret += "*x"
            power = len(pol) - i - 1
            if power > 1:
                ret += "^" + str(power)
    return ret


def edges(lst):
    max = lst[0][0]
    min = lst[0][0]
    for i in lst:
        if i[0] > max:
            max = i[0]
        if i[0] < min:
            min = i[0]
    return (min, max)


def plot(pol, lab, min, max):
    x = np.linspace(min, max, 1000)
    y = x*0
    for i in range(len(pol)):
        y += pol[i] * (x**(len(pol)-i-1))
    
    plt.plot(x,y, 'r', label=lab)
    plt.legend(loc='upper left')


def compute(lst):
    plt.title("Lagrange polynomial")
    pol = generate_polynomial(lst)

    print_line()
    print("The polynomial formula is:")
    str = polynom_to_str(pol)
    print(str)
    print_line()
    edge = edges(lst)

    plot(pol, str, edge[0], edge[1])
    plt.scatter(*zip(*lst))

    plt.show()


def prompt():
    list_of_tuples = []
    while 1:
        try:
            inp = input(">")
        except EOFError:
            print("")
            break

        if re.match(r"^-?\d+.?\d* -?\d+.?\d*$", inp):
            list_of_tuples.append(tuple(map(float, inp.split())))

        elif inp == "h":
            print_help()

        elif inp == "v":
            print_line()
            print("The points are:")
            for a in list_of_tuples:
                print("x = " + frm(a[0]) + "; y = " + frm(a[1]) + ";")
            print_line()

        elif inp == "c":
            if len(list_of_tuples) < 2:
                print("You need to input at least two points to compute.")
            else:
                try:
                    compute(list_of_tuples)
                except ZeroDivisionError:
                    print("The Lagrange polynomial is impossible to compute for this set of points.")

        elif inp == "d":
            list_of_tuples = []

        elif inp == "q":
            break

        else:
            print_err()
    


def main():
    print("Welcome to the Lagrange polynomial calculator. To see the list of commands, type \"h\". To quit, type \"q\".")
    print_line()
    prompt()


main()
