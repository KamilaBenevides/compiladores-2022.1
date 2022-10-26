
class JumpIndex(object):
    def __init__(self, small_jump=None, big_jump=None, jump_big=False):
        """This class stores a token jump indexes

        When jumping tokens, sometimes you need jump big or jump small. So
        this class is needed to control how far it jumps.

        :param bool jump_big: If jump_big then not jump small.
        :param int small_jump: small jump index.
        :param int big_jump: big jump index.
        """
        self.jump_big = jump_big
        self.big_jump_index = big_jump # indice do fim ou do começo do bloco
        self.small_jump_index = small_jump # indice do proximo token
    
    def get_jump_index(self):
        if self.jump_big:
            return self.big_jump_index
        return self.small_jump_index

    def __str__(self):
        return f"{self.jump_big}, b:{self.big_jump_index}, s:{self.small_jump_index}"