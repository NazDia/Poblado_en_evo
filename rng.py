import time
import math

class SubtractiveRNG:
    def __init__(self, seed=None):
        if seed is None:
            seed = time.perf_counter()

        while seed > 1.1:
            seed /= 10

        seed -= 0.1
        self.current = 1
        self.seed_array = [0 for _ in range(56)]
        self.MSEED = 0.161803398
        
        mj = mk = 0

        mj = self.MSEED - seed if self.MSEED - seed > 0 else self.MSEED - seed + 1
        self.seed_array[55]
        mk = 0.01
        for i in range(1, 56):
            j = (21 * i) % 55   # Primos relativos, por lo cual cada 21 * i 
                                # resultara en un j distinto y se ocuparan todos
                                # los posibles j

            self.seed_array[j] = mk
            mk = mj - mk if mj - mk > 0 else mj - mk + 1

        for _ in range(4):
            for i in range(1, 56):
                self.seed_array[i] -= self.seed_array[1 + (i + 21) % 55]
                if self.seed_array[i] < 0:
                    self.seed_array[i] += 1

    
    def random(self):
        self.seed_array[self.current] -= self.seed_array[1 + (self.current + 21) % 55]
        if self.seed_array[self.current] < 0:
            self.seed_array[self.current] += 1

        ret = self.seed_array[self.current]
        self.current += 1
        self.current %= 56
        if self.current == 0:
            self.current += 1
        return ret

    def randint(self, li, ls):
        if ls <= li:
            raise ValueError("Limite superior es menor o igual que el limite inferior")

        r = self.random()
        r *= (ls + 1 - li)
        ret = r.__trunc__()
        ret += li
        return ret

    def exp_random(self, l):
        return  (-1 / l) * math.log1p(-self.random())