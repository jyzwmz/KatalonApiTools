#!/usr/bin/python
# -*- coding: utf-8 -*-

from faker import Faker
import csv
from multiprocessing import Pool #导入进程池
import datetime


def mycallback(x):
    print(x)
    csv_write.writerow(x)


def sayHi(num):
    w = [str(num), str(num + 1), str(num + 2)]
    return w


if __name__ == '__main__':
    e1 = datetime.datetime.now()
    csv_file = open('Text.csv', 'w')
    csv_write = csv.writer(csv_file)
    p = Pool(4)

    for i in range(10):
        p.apply_async(sayHi, (i,), callback=mycallback)  # sayHi是我们进程运行的对象，callback=mycallback这里是当
    p.close()
    p.join()
    e2 = datetime.datetime.now()
    print((e2-e1))
    csv_file.close()

