#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymssql
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
        fake.company()+','+ fake.date_time_between(start_date="now", end_date="+1y", tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")


    print vContent
    #print len(str(vContent))
    #sys.exit()
    for i in range(num):
        sql="""insert into TestUser(sales_,name_,phone_,company_,date_) 
        values('%d',N'%s',N'%s',N'%s',N'%s')"""\
            %(random.randint(100,10000),fake.name(),fake.phone_number(),fake.company(),\
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
    print(str(i) + "=" + "程序从 " + start + ' 开始运行,运行时间为：' + timeStr)

    conn.commit()
if __name__ == '__main__':
    # 建立连接并获取cursor
    conn = pymssql.connect("10.57.17.204", "sa", "Td@123456", "TestDB")

    #conn = pymysql.connect(host="localhost", port=3306, user="pig", password="123456", db="complexTestData",
                           #charset="utf8")
    cursor = conn.cursor()
    #print cursor
    # 查询记录
    #cursor.execute('select * from Inventory where id=1')
    # 获取一条记录
    #row = cursor.fetchone()
    # 循环打印记录(这里只有一条，所以只打印出一条)
    #while row:
        #print("ID=%d, Name=%s" % (row[0], row[1]))
        #row = cursor.fetchone()
    #genData(1)
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
    for i in range(1000):
        genData(999)
    cursor.close()
    conn.close()


