import random

class PKeysFactory:
    def __init__(self):
        self.dict = '0123456789abcdef'
        self.maxLength = len(self.dict) - 1

    def produce(self, maxIndex):
        index = random.randint(0, self.maxLength)
        result = ''
        i = 0
        while(i < maxIndex):
            index = random.randint(0, self.maxLength)
            result = result + self.dict[index]
            i = i + 1
        return result
