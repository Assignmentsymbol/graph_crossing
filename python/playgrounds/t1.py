import time

import IntersectAlgorithm

a = 0
t0 = time.time()
for i in range(0,10000):
   for j in range(0,10000):
      a += 1
      # IntersectAlgorithm.doIntersect(1,1,2,2)
t1 = time.time()
for i in range(0,2700):
    for j in range(0,20):
        a += 1
        IntersectAlgorithm.doIntersect(1,1,2,2)
t2 = time.time()
print(f'delta1 = {t1-t0:.5f}, delta2 = {t2-t1:.5f} ratio = {(t1-t0)/(t2-t1):.5f}')
print("+++++++")


