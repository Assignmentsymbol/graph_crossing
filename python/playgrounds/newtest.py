pos = {"a":1,"b":2}
posc = pos.copy()
posc["a"] = 3
print(posc)
print(pos)
lis = [(1,2),(2,3),(3,4)]
ls2 = lis.copy()
lis[0] = 5,6
print(lis)
print(ls2)
# tuples are not modifiable