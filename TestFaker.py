#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
from faker import Faker
import datetime
import random



def genData(num):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    fake=Faker("zh-CN")
    #fake=Faker()
    starttime = datetime.datetime.now()
    print fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")

    vContent = str(random.randint(100,10000))+','+fake.name()+','+fake.phone_number()+','+ \
        fake.date_time_between(start_date="now", end_date="+90y", tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")+','+ \
        fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")+ ','+ \
        fake.date_time_between(start_date="now", end_date="+1y", tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")


    print vContent
    print len(str(vContent))
    #sys.exit()
    for i in range(num):
        sql="""insert into user1(name_,sales_,date_valid_,date_invalid_) 
        values('%s','%d','%s','%s')"""\
            %(fake.name()+str(random.randint(100,10000)).encode("utf-8"),random.randint(100,10000),\
              fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),\
              fake.date_time_between(start_date="now", end_date="+90y", tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql)
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

    conn.commit()
if __name__ == '__main__':
    conn = pymysql.connect(host="localhost", port=3306, user="pig", password="123456", db="complexTestData",
                           charset="utf8")
    cursor = conn.cursor()
    print cursor
    # 这里给出表结构，如果使用已存在的表，可以不创建表。
    # sql="""
    # create table user(
    # id int PRIMARY KEY auto_increment,
    # username VARCHAR(20),
    # password VARCHAR(20),
    # address VARCHAR(35)
    # )
    # """
    # cursor.execute(sql)
    for i in range(10):
        genData(99999)
    cursor.close()
    conn.close()


