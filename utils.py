import numpy as np
import numpy.random as nrand

random_list = nrand.random(size=10000000).tolist()

def get_random():
    global random_list
    if len(random_list) == 0:
        random_list = nrand.random(size=10000000).tolist()
    return random_list.pop()
