import argparse
import random
import logging
from math import exp
from zipf import zipf
from kRR import kRR
from MGA import MGA
from OUE import OUE

logging.basicConfig(level=logging.INFO)

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
	def __init__(self, m, d, promotedItems, protocol):
		self.m = m
		self.d = d
		self.promotedItems = promotedItems
		self.Items = [0] * m
		self.protocol = protocol

	def getItems(self):
		for i in range(self.m):
			self.Items[i] = self.protocol.getItem(self.promotedItems)
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
		self.true_f_before_attack = []
		self.estimated_f_before_attack = []
		self.estimated_f_after_attack = []
		self.diff_f_vs_estimated_f = []
	
	def Algorithm(self):
		"""
		The function of our Algorithm.
		"""
		pass

	def validation(self):
		"""
		The function to count the frequency

		"""
		self.true_f_before_attack = self.good_guys.protocol.aggregate(self.good_guys.initItems)
		self.estimated_f_before_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems)
		self.estimated_f_after_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems + self.bad_guys.Items)
		for i, j in zip(self.estimated_f_before_attack, self.estimated_f_after_attack):
			self.diff_f_vs_estimated_f.append(i - j)
		self.diff_f_vs_estimated_f_norm = [(i - min(self.diff_f_vs_estimated_f)) / (max(self.diff_f_vs_estimated_f) - min(self.diff_f_vs_estimated_f)) for i in self.diff_f_vs_estimated_f]

		
	def run(self):
		"""
		The function to run the whole process.

		Returns: 
			overall gain G
		"""
		for r in range(self.round):

			logging.info(f"======= Round {r+1} ========")

			self.good_guys.getInitItems()
			self.good_guys.getPerturbedItems()

			logging.info(f"good_guys: {self.good_guys.initItems}")
			logging.info(f"pertubed: {self.good_guys.perturbedItems}")

			self.bad_guys.getItems()
			logging.info(f"bad_guys: {self.bad_guys.Items}")

			# our algorithm
			self.Algorithm()
			
			self.validation()
			#logging.info(f'diff_f_vs_estimated_f: {self.diff_f_vs_estimated_f}')
			logging.info(f'diff_f_vs_estimated_f_norm: {self.diff_f_vs_estimated_f_norm}')


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int, default=10, metavar='n', help='number of good guys, default = 10')
	parser.add_argument('-p1', type=str, default='kRR', metavar='good_protocol', help='protocol of good guys, \'kRR\' or \'OUE\', default = \'kRR\'')
	parser.add_argument('-m', type=int, default=3, metavar='m', help='number of bad guys, default = 3')
	# parser.add_argument('-p2', type=str, default='MGA', metavar='bad_protocol',help='protocol of bad guys')
	parser.add_argument('-d', type=int, default=10, help='size of domain, default = 10')
	parser.add_argument('--promote', type=str, default="3,4,5", metavar='promoted_items', help='the items attackers want to promoted, separate by \',\' default = \'3,4,5\'')
	parser.add_argument('-r', type=int, default=10, metavar='round', help='number of rounds, default = 10')
	args = parser.parse_args()

	return args

if __name__ == '__main__':
	# help(Center)
	args = parse_arguments()

	promoted_items = [int(i) for i in args.promote.split(',')]
	promoted_items.sort()

	if promoted_items != None and args.d <= promoted_items[-1]:
		logging.error('promoted item\'s index cannot exceed the size of domain!')
		exit(-1)

	good_protocol = kRR(d=args.d) if args.p1 == 'kRR' else OUE(d=args.d)
	bad_protocol = MGA(d=args.d, attack_protocol=args.p1)

	good_guys = GoodGuys(n=args.n, d=args.d, distribution=zipf(d=args.d), protocol=good_protocol)
	bad_guys = BadGuys(m=args.m, d=args.d, promotedItems=promoted_items, protocol=bad_protocol)

	center = Center(round=args.r, good_guys=good_guys, bad_guys=bad_guys)
	center.run()

