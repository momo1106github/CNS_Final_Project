import argparse
import random
from math import exp
from zipf import zipf
from kRR import kRR
from MGA import MGA
from OUE import OUE

class GoodGuys:
	def __init__(self, n, d, distribution, protocol):
		self.n = n
		self.d = d
		self.initItems = [0] * n
		self.encodedItems = [0] * n
		self.perturbedItems = [0] * n
		self.distribution = distribution
		self.protocol = protocol

	def getInitItems(self):
		"""
		The function to get each good guys's initial Items.

		Parameters:
			num (int): number of good/bad guys
			guys: array of good/bad guys

		Returns: 
			array of good/bad guys with new values
		"""
		for i in range(self.n):
			self.initItems[i] = self.distribution.getValue()
		return self.initItems

	def getPerturbedItems(self):
		for i in range(self.n):
			self.encodedItems[i] = self.protocol.encode(self.initItems[i])
			self.perturbedItems[i] = self.protocol.perturb(self.encodedItems[i])
		return self.perturbedItems

class BadGuys:
	def __init__(self, m, d, promotedItems, attack_protocol, protocol):
		self.m = m
		self.d = d
		self.promotedItems = promotedItems
		self.Items = [0] * m
		self.attack_protocol = attack_protocol
		self.protocol = protocol

	def getItems(self):
		for i in range(self.m):
			self.Items[i] = self.protocol.getItem(self.attack_protocol, self.promotedItems)
		return self.Items

class Center:
	"""
		This class runs the LDP protocol over multiple rounds.
	"""

	def __init__(self, round, good_guys, bad_guys):
		"""
		The constructor for LDP_Model class.
		"""
		self.round = round
		self.n = good_guys.n
		self.m = bad_guys.m
		self.good_guys = good_guys
		self.bad_guys = bad_guys
		self.estimated_f_before_attack = [0] * self.n
		self.estimated_f_after_attack = [0] * (self.n + self.m)

	
	def Algorithm(self):
		"""
		The function of our Algorithm.
		"""
		pass

	def validation(self):
		"""
		The function to validate the gain (for single round?).

		Returns:
			gain
		"""
		self.estimated_f_before_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems)
		self.estimated_f_after_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems + self.bad_guys.Items)
		
		# print (self.estimated_f_before_attack)
		# print (self.estimated_f_after_attack)
		return [self.estimated_f_after_attack[i] - self.estimated_f_before_attack[i] for i in range(len(self.estimated_f_before_attack))]

	def run(self):
		"""
		The function to run the whole process.

		Returns: 
			overall gain G
		"""
		for r in range(self.round):

			print ("==== Round", r+1, "====")

			self.good_guys.getInitItems()
			self.good_guys.getPerturbedItems()

			print ("good_guys:", self.good_guys.initItems)
			print ("pertubed:", self.good_guys.perturbedItems)

			self.bad_guys.getItems()
			print ("bad_guys:", self.bad_guys.Items)

			# our algorithm
			self.Algorithm()
			
			print (self.validation())


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int, default=10, help='number of good guys')
	parser.add_argument('-m', type=int, default=1, help='number of bad guys')
	parser.add_argument('-p1', type=str, default='', help='protocol of good guys')
	parser.add_argument('-p2', type=str, default='', help='protocol of bad guys')
	parser.add_argument('-r', type=int, default=10, help='number of rounds')
	args = parser.parse_args()

	return args

if __name__ == '__main__':
	# help(Center)
	# args = parse_arguments()

	# good_protocol = None
	# bad_protocol = None
	# if args.p1 == 'SingleRoundFlipCoin':
	# 	good_protocol = SingleRoundFlipCoin()

	# if args.p2 == 'SingleRoundFlipCoin':
	# 	bad_protocol = SingleRoundFlipCoin()
	
	good_guys = GoodGuys(n=10, d=10, distribution=zipf(d=10), protocol=OUE(d=10))
	bad_guys = BadGuys(m=3, d=10, promotedItems=[3, 4], attack_protocol="OUE", protocol=MGA(d=10))

	center = Center(round=2, good_guys=good_guys, bad_guys=bad_guys)
	center.run()

