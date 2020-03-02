import time
from tqdm import tqdm

'''
loop = tqdm(total = 5000, position = 0, leave = False)
for k in range(5000):
    loop.set_description("loading...".format(k))
    loop.update(1)

loop.close()
'''
arq = open('a.txt')

for i in tqdm(arq, leave = True):
    time.sleep(1)
    print(i)
    pass