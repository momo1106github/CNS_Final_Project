import random

class zipf():
    """
    This class implement some methods for zipf distribution.
    """

    def __init__(self, d=10):
        """
        The constructor for zipf class.

        Attributes:
            category (int): How many category that want to be generated.
        """
        
        self.d = d
        self.indices = [i for i in range(d)]
        self.weights = [1 / w for w in range(1, d + 1)]

    def gen_data(self, amount):
        """
        The function to generate data which distribution follow zipf's law.

        Parameters:
            amount (int): Total amount that want to be generated.

        Returns:
             Data which distribution follow zipf's law.
        """

        return random.choices(self.indices, weights=self.weights, k=amount)

    def getValue(self):
        """
        The function to get an index following zipf's law.

        Returns:
            Index(range from 0 to self.d - 1).
        """
        return random.choices(self.indices, weights=self.weights, k=1)[0]


# if __name__ == "__main__":
#     d = 10
#     amount = 10000
#     total = [0] * d

#     z = zipf(category)
#     data = z.gen_data(amount)
#     for d in data:
#         total[d] += 1
#     print(total)
