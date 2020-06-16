import random

'''
protocol : KRR or OUE
item_list : KRR 1 個, OUE 數個
return KRR 一個 [index]，OUE [1,0,0,1,0,0,0,0,1]
'''

class MGA():
    """
    This class implement some methods for MGA.
    """

    def __init__(self, d=10):
        """
        The constructor for MGA class.

        Attributes:
            category (int): How many category that want to be generated.
        """
        
        self.d = d

    def getItem(self, protocol, item_list):
        """
        The function to encode items that want to be promoted.

        Parameters:
            protocol (str) : Which protocol to follow.
            item_list (list of int): Items that want to be send.

        Returns:
            Suggested item to be sent (list of int)
        """
        if (protocol == "kRR"):
            return random.choice(item_list)
        elif (protocol == "OUE"):
            bit_vector = [0] * self.d
            for item_index in item_list:
                bit_vector[item_index] = 1

            cnt_one = bit_vector.count(1)
            p = (4 - cnt_one) / (len(bit_vector) - cnt_one)

            for i in range(len(bit_vector)):
                if bit_vector[i] == 0:
                    bit_vector[i] = 1 if random.random() <= p else 0 
            return bit_vector 
        else:
            assert(False)

