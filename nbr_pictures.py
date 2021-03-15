#!/usr/bin/env python2
import numpy as np
import os

Max = 21
counter = [0] * (Max+1)
for root, dirs, files in os.walk("raw"):
	for img in files:
		for N in range(1, (Max+1)):
			if ("000"+str(N) in img and N < 10) or ("00"+str(N) in img and 9 < N < 100) or ("0"+str(N) in img and 99 < N < 1000):
				counter[N] += 1
print("N.:")
print(range(1,Max))
print("Counter:")
print(counter[1:])