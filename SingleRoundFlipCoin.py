import random

class SingleRoundFlipCoin():
    """
    This class implement some methods for single round flip coin.
    """

    def __init__(self):
        """
        The constructor for SingleRoundFlipCoin class.
        """

        self.HEAD = 0
        self.TAIL = 1

    def get_rand_res(self, face = 0, prob = 0.5):
        """
        The function to get randomized response.

        Parameters:
            face (int): Coin face (Head or Tail) that is thrown by user.
            prob (float): Probability (range from 0 to 1) of showing user's real answer.

        Returns:
            Randomized response(0 for Head, 1 for Tail).
        """

        first_toss = random.choices([self.HEAD, self.TAIL], weights = [prob, 1 - prob], k = 1)[0]
        if (first_toss == self.HEAD):
            return int(not(not(face)))

        second_toss = random.choices(population = [self.HEAD, self.TAIL], weights = [0.5, 0.5], k = 1)[0]
        return int(not(not(second_toss)))

help(SingleRoundFlipCoin)
