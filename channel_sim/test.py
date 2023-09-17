import numpy as np

# 0 -> no error
# 1 -> error
BER = 0.1

for _ in range(100):
    print(np.random.choice([0, 1], 1, p=[1 - BER, BER])[0])
