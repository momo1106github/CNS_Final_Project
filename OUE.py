import random
from math import exp

class OUE():
    """
    This class implement some methods for OUE.
    """

    def __init__(self, d=10, epsilon=1.09):
        """
        The constructor for OUE class.

        Attributes:
            d (int): How many category that want to be generated.
            epsilon (double): Epsilon used to calculate probability q.
        """
        
        self.d = d
        self.epsilon = epsilon
        self.p = 0.5
        self.q = 1 / (exp(epsilon) + 1)

    def encode(self, item):
        """
        The function to encode items that want to be promoted.

        Parameters:
            item (int): Item that want to be promoted.

        Returns:
            Encoded items (list of int)
        """

        encoded_item = [0] * self.d
        encoded_item[item] = 1

        return encoded_item

    def perturb(self, encoded_item):
        """
        The function to perturb encoded items. 
        For each bit of the encoded binary vector, if it is 1, then it remains 1 with a probability p.
        Otherwise if the bit is 0, it is flipped to 1 with a probability q.

        Parameters:
            encoded_item (list of int): Encoded items that are going to be perturbed.

        Returns:
            Perturbed items (list of int)
        """

        assert(self.d == len(encoded_item))

        indices = [1, 0]
        perturbed_item = list(encoded_item)

        for i in range(len(perturbed_item)):
            if perturbed_item[i] == 1:
                perturbed_item[i] = random.choices(indices, weights = [self.p, 1 - self.p], k = 1)[0]
            elif perturbed_item[i] == 0:
                perturbed_item[i] = random.choices(indices, weights = [self.q, 1 - self.q], k = 1)[0]
            else:
                assert(False)

        return perturbed_item

    def aggregate(self, perturbed_items):
        """
        The function to aggregate items. 

        Parameters:
            perturbed_items (list of int): Perturbed items that are going to be check.
        """
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



# if __name__ == "__main__":
#     d = 10 # There are 10 category, including item0, item1, ..., item9
#     item = 1 # Want to promote item1
#     frequency = [0] * d # Frenquency of each item
#     n = 100
    
#     for i in range(n):
#         OUE_instance = OUE(d)
#         encoded_item = OUE_instance.encode(item)
#         perturbed_item = OUE_instance.perturb(encoded_item)
#         print (perturbed_item)


#     for item_index in range(d):
#         frequency[item_index] = ((frequency_estimator[item_index] / n) - q) / (p - q)

#     print(frequency_estimator)
