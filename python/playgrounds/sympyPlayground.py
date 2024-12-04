from pprint import pprint
from sympy import *
import sympy
from sympy.abc import i, k, m, n, x, y, A
from sympy.polys.polyoptions import Series
from sympy import Sum, factorial, oo, IndexedBase, Function, Integer
import numpy as np


# def f(x):
#     return 3*x;
def m(x):

    x_list = [1, 2, 3, 4, 5]
    return x_list[x-1]

class versin(Function):
   @classmethod
   def eval(cls, x):
       # If x is an integer multiple of pi, x/pi will cancel and be an Integer
       n = x/pi
       if isinstance(n, Integer):
           return 1 - (-1)**n
class f1(Function):
    @classmethod
    def eval(cls, x):
        if x == 0 or x == 1:
            return 0
        else:
            return 1


# print(Sum(f1(k),(k,0,1)).doit())
def o(x):
    return x+1


x, i = symbols("x i")
s = Sum(Indexed('x',0)+Indexed('x',o(i)),(i,0,1))
f = lambdify(x, s)
b = [0,2,3,3]
print(f(b))
# print(Sum(exp,(a,0,1)).doit())

print(Sum(versin(1),(k,0,3)).doit())



# print(Sum(m(k),(k,1,2)).doit())

# ctrl+tab run
# x_list = [1,2,3,4,5]
k_list = [2,4,6,8,10]
L = 3

list_to_sum = [1,3,5,7]
# f = Function('f')
y = Function('y')
print(Sum(y(k),(k,0,1)).doit())

pprint(y.diff(x))

# Sum(f(n), (n, 0, 3)).doit()
# Sum(f(n), (n, 0, oo)).doit()
f = IndexedBase('f')
y = Sum(f, (n, 0, 3)).doit()

print(y)