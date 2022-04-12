import math
import timeit
import random
import sys
import functools

value_hack = -1

def bit_len(test_value):

    global value_hack

    v = test_value

    previous_v = v - 1
    i = 1
    while v != previous_v:
        previous_v = v
        v |= (v >> i)
        i += 1

    v += 1
    b = math.log(v, 2)
    value_hack = b
    return b

test_value = 618970019642690137449562111

for _ in range(0, 100):
    t = timeit.timeit(lambda: bit_len(test_value))
    print(f"{test_value}:{value_hack:.0f}:{t}")
    test_value = random.randrange(0, sys.maxsize)

