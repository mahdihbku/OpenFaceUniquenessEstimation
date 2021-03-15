#!/usr/bin/env python2
import pandas as pd
import os
import math


def compute_H(V, k):		# eq. 3
	h = 0
	for j in range(k):
		p = 1.0 * V.count(j) / len(V)
		h += 0 if p == 0 else p * math.log(1/p,2)	# TODO to be checked (p==0)!!!!!!!!!!!!!!
	return h


for nbr_bits in [1,2,3,4]:
	# Loading all reps from the corresponding file
	all_reps = pd.read_csv("lloyd_quantized_reps_"+str(nbr_bits)+"bits.csv", header=None).as_matrix()
	# all_reps = pd.read_csv("reps_"+str(nbr_bits)+"bits.csv", header=None).as_matrix()

	for nbr_pics_per_person in [2,4,6,8,10]:
		# Selecting reps of persons having at least nbr_pics_per_person pictures
		reps_to_use = []
		counter = 0
		for root, dirs, files in os.walk("raw"):
			for img in files:
				counter += 1
				if ("000"+str(nbr_pics_per_person) in img and nbr_pics_per_person < 10) or ("00"+str(nbr_pics_per_person) in img and 9 < nbr_pics_per_person < 100):
					for i in range(nbr_pics_per_person):
						reps_to_use.append(all_reps[counter-i])

		# Computing V. V is a matrix of size: 3360 x 128
		V = []
		m = 128
		for i in range(m):
			sub_V = []
			for rep in reps_to_use:
				sub_V.append(rep[i])
			V.append(sub_V)

		# Computing H(V) = sum(H(Vi))		# eq. 6
		k = 2**nbr_bits
		H_V = 0
		for i in range(m):
			H_V += compute_H(V[i], k)

		# Computing H(V|S)					#eq. 7
		nbr_persons = len(reps_to_use)/nbr_pics_per_person		# 1680
		H_VS = 0
		for i in range(nbr_persons):
			for j in range(m):
				H_VS += compute_H(V[j][i*nbr_pics_per_person : i*nbr_pics_per_person+nbr_pics_per_person], k)
		H_VS /= nbr_persons

		# Computing I(S;V)
		I = H_V - H_VS						# eq. 8
		print("nbr_bits= {} nbr_pics_per_person={} I= {}".format(nbr_bits, nbr_pics_per_person, I))