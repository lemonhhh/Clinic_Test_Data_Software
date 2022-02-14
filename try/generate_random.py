import random
import numpy as np


#正常的
def generate_random_number(n,min,max)  -> list:
    random_numbers = []
    for i in range(n):
        rn = random.uniform(min,max)
        random_numbers.append(np.round(rn,3))
    return random_numbers

'''
pt 
秒数:11-14 ，需与正常对照超过3s以上异常
'''
pt = []
pt = generate_random_number(10,11,14)
print("pt",pt)
'''
aptt
秒数:25-37 ，需与正常对照超过10s以上异常
'''
aptt = []
aptt = generate_random_number(10,25,37)
print("aptt",aptt)
'''
fig
正常：2-4
'''
fib = []
fib = generate_random_number(10,2,4)
print("fib",fib)

'''
tt
秒数:12-16 ，需与正常对照超过3s以上异常
'''
tt = []
tt = generate_random_number(10,12,16)
print("tt",tt)

