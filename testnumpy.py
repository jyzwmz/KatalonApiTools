#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import time

a = np.random.rand(1000000)
b = np.random.rand(1000000)

time_cur = time.time()
c = a.dot(b)
time_later = time.time()
print(c)
vec_time = 1000*(time_later-time_cur)
print("Vectorized is " + str(vec_time) + "ms")

print()
c = 0
time_cur = time.time()
for i in range(a.size):
    c += a[i] * b[i]
time_later = time.time()
print(c)
loop_time = 1000*(time_later-time_cur)
print("Loop is " + str(loop_time) + "ms")
print()
print("times is " + str(loop_time/vec_time))