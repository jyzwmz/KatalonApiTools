#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
from faker import Faker
import datetime
import threading
import time

def insert(nCount):
    time_now = datetime.datetime.now()
    print nCount,time_now
    #time.sleep(5)
    conn = pymysql.connect(host="localhost", port=3306, user="pig", password="123456", db="complexTestData",
                           charset="utf8")
    cursor = conn.cursor()
    conn.ping(True)
    fake = Faker("zh-CN")
    starttime = datetime.datetime.now()
    nCnt=0
    for i in range(nCount):
        sql = """insert into user(username,password,address) 
        values('%s','%s','%s')""" \
              % (fake.user_name(), fake.password(special_chars=False), fake.address())
        cursor.execute(sql)
        nCnt+=1
        print 'nCnt='+str(nCnt)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    for thread in range(10):
        t = threading.Thread(target=insert, args=(100000,))
        t.start()
    t.join()
    endtime = datetime.datetime.now()
    seconds = (endtime - starttime).seconds
    start = starttime.strftime('%Y-%m-%d %H:%M')
    # 100 秒
    # 分钟
    minutes = seconds // 60
    second = seconds % 60
    print((endtime - starttime))
    timeStr = str(minutes) + '分钟' + str(second) + "秒"
    print("程序从 " + start + ' 开始运行,运行时间为：' + timeStr)
    #t = threading.Thread(target=insert, args=('100',))
    #t.start()
    #t = threading.Thread(target=insert, args=('200',))
    #t.start()
    #t = threading.Thread(target=insert, args=('300',))
    #t.start()
    #t.join()