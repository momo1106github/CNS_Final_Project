import random
from math import exp

class kRR:
	def __init__(self, d=10, epsilon=1.09):
		self.d = d
		self.epsilon = epsilon
		self.p = exp(epsilon) / (d - 1 + exp(epsilon))
		self.q = 1 / (d - 1 + exp(epsilon))

	def encode(self, item):
		return item

	def perturb(self, encoded_item):
		if random.random() <= self.p:
			return encoded_item
		else:
			perturbed_item = random.randint(0, self.d-1)
			while perturbed_item == encoded_item:
				perturbed_item = random.randint(0, self.d-1)

			return perturbed_item 

	def aggregate(self, perturbed_items):
		n = len(perturbed_items)
		estimated_f = []
		for v in range(self.d):
			p_ = 0
			for i in range(n):
				if perturbed_items[i] == v:
					p_ += 1

			p_ /= n
			estimated_f.append((p_ - self.q) / (self.p - self.q))

		return estimated_f

