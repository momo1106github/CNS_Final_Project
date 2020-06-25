import argparse
import random
import logging
from sklearn.metrics import confusion_matrix
from math import exp, log
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
		self.d = good_guys.d
		self.good_guys = good_guys
		self.bad_guys = bad_guys
		self.true_f_before_attack = []
		self.estimated_f_before_attack = []
		self.estimated_f_after_attack = []
		self.diff_f_vs_estimated_f_before_attack = []
		self.diff_f_vs_estimated_f_before_attack_norm = []
	
	def count_frequency(self, P):
		f = [0] * self.d
		for i in P:
			f[i] += 1
		return f

	def D_KL(self, P, Q):
		sum = 0
		for a in range(self.d):
			try:
				sum += P[a] * log(P[a] / Q[a])
			except:
				sum += 0
		return sum

	def GJS(self, P, Q, alpha):
		Q_ = [(P[i] + alpha*Q[i]) / (1 + alpha) for i in range(self.d)]
		# print ('== in GJS ==')
		# print ('P :', P)
		# print ('Q :', Q)
		# print ('Q_ :', Q_)
		return self.D_KL(P, Q_) + alpha * self.D_KL(Q, Q_)

	def Algorithm(self):
		"""
		The function of our Algorithm.
		"""
		N = 300
		P = [self.good_guys.perturbedItems[i] for i in range(N)]
		Q = [self.bad_guys.Items[i] for i in range(N)]

		# print ('P :', P)
		# print ('Q :', Q)

		P_hat = self.count_frequency(P)
		Q_hat = self.count_frequency(Q)

		print ('P_hat :', P_hat)
		print ('Q_hat :', Q_hat)

		threshold = 10

		numTest = 1000
		n = 300

		y_true = [0] * (int(numTest*0.9)) + [1] * (int(numTest*0.1)) # 0->good, 1->bad
		y_predict = []

		mx_good = 0
		mn_good = 9999999999999

		for t in range(int(numTest * 0.9)): # test good guys
			rand_index = [i for i in range(self.n)]
			random.shuffle(rand_index)
			rand_index = rand_index[:n]

			Pi_xn = self.count_frequency([self.good_guys.perturbedItems[i] for i in rand_index])
			y_predict.append(0 if self.GJS(Pi_xn, Q_hat, N / n) >= threshold else 1)
			mx_good = max(mx_good, self.GJS(Pi_xn, Q_hat, N / n))
			mn_good = min(mn_good, self.GJS(Pi_xn, Q_hat, N / n))

		print ('mx_good :', mx_good)
		print ('mn_good :', mn_good)

		mx_bad = 0
		mn_bad = 9999999999999

		for t in range(int(numTest * 0.1)): # test bad guys
			rand_index = [i for i in range(self.m)]
			random.shuffle(rand_index)
			rand_index = rand_index[:n]

			Pi_xn = self.count_frequency([self.bad_guys.Items[i] for i in rand_index])
			y_predict.append(0 if self.GJS(Pi_xn, Q_hat, N / n) >= threshold else 1)
			mx_bad = max(mx_bad, self.GJS(Pi_xn, Q_hat, N / n))
			mn_bad = min(mn_bad, self.GJS(Pi_xn, Q_hat, N / n))

		print ('mx_bad :', mx_bad)
		print ('mn_bad :', mn_bad)

		print ("confusion_matrix:\n",confusion_matrix(y_true, y_predict))

	def validation(self):
		"""
		The function to count the frequency

		"""
		self.f_before_attack = self.good_guys.protocol.aggregate(self.good_guys.initItems)
		self.estimated_f_before_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems)
		self.estimated_f_after_attack = self.good_guys.protocol.aggregate(self.good_guys.perturbedItems + self.bad_guys.Items)
		for i, j in zip(self.estimated_f_before_attack, self.f_before_attack):
			self.diff_f_vs_estimated_f_before_attack.append(i - j)
		self.diff_f_vs_estimated_f_before_attack_norm = [(i - min(self.diff_f_vs_estimated_f_before_attack)) / (max(self.diff_f_vs_estimated_f_before_attack) - min(self.diff_f_vs_estimated_f_before_attack)) for i in self.diff_f_vs_estimated_f_before_attack]

		
	def run(self):
		"""
		The function to run the whole process.

		Returns: 
			overall gain G
		"""
		for r in range(self.round):

			print (f"======= Round {r+1} ========")

			self.good_guys.getInitItems()
			self.good_guys.getPerturbedItems()

			print (f"good_guys: {self.good_guys.initItems}")
			print(f"pertubed: {self.good_guys.perturbedItems}")

			self.bad_guys.getItems()
			print (f"bad_guys: {self.bad_guys.Items}")

			# GSJ for kRR
			print (type(self.good_guys.protocol))
			if type(self.good_guys.protocol) == kRR:
				self.Algorithm()
			
			#self.validation()
			#logging.info(f'diff_f_vs_estimated_f: {self.diff_f_vs_estimated_f}')
			#print ('diff_f_vs_estimated_f_norm:', [round(i, 3) for i in self.diff_f_vs_estimated_f_before_attack_norm])


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

