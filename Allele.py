class Allele:
    N = 0

    def __init__(self, effect=0):
        self.index = Allele.N
        self.effect = effect
        Allele.N += 1
