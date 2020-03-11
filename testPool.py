#!/usr/bin/python
# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from socketpool import ConnectionPool, TcpConnector
import multiprocessing
import logging
import time
from Queue import Queue
import datetime

class PoolException(Exception):
    pass


class Pool(object):
    '''一个数据库连接池'''

    def __init__(self, maxActive=5, maxWait=None, init_size=0, db_type="kafka", **config):
        self.__freeConns = Queue(maxActive)
        self.maxWait = maxWait
        self.db_type = db_type
        self.config = config
        if init_size > maxActive:
            init_size = maxActive
        for i in range(init_size):
            self.free(self._create_conn())

    def __del__(self):
        print("__del__ Pool..")
        self.release()

    def release(self):
        '''释放资源，关闭池中的所有连接'''
        print("release Pool..")
        while self.__freeConns and not self.__freeConns.empty():
            con = self.get()
            con.release()
        self.__freeConns = None

    def _create_conn(self):
        '''创建连接 '''
        if self.db_type in dbcs:
            return dbcs[self.db_type](**self.config);

    def get(self, timeout=None):
        '''获取一个连接
        @param timeout:超时时间
        '''
        if timeout is None:
            timeout = self.maxWait
        conn = None
        if self.__freeConns.empty():  # 如果容器是空的，直接创建一个连接
            conn = self._create_conn()
        else:
            conn = self.__freeConns.get(timeout=timeout)
        conn.pool = self
        return conn

    def free(self, conn):
        '''将一个连接放回池中
        @param conn: 连接对象
        '''
        conn.pool = None
        if (self.__freeConns.full()):  # 如果当前连接池已满，直接关闭连接
            conn.release()
            return
        self.__freeConns.put_nowait(conn)


from abc import ABCMeta, abstractmethod


class PoolingConnection(object):
    def __init__(self, **config):
        self.conn = None
        self.config = config
        self.pool = None

    def __del__(self):
        self.release()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def release(self):
        print("release PoolingConnection..")
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        self.pool = None

    def close(self):
        if self.pool is None:
            raise PoolException("连接已关闭")
        self.pool.free(self)

    def __getattr__(self, val):
        if self.conn is None and self.pool is not None:
            self.conn = self._create_conn(**self.config)
        if self.conn is None:
            raise PoolException("无法创建数据库连接 或连接已关闭")
        return getattr(self.conn, val)

    @abstractmethod
    def _create_conn(self, **config):
        pass


class KafkaPoolConnection(PoolingConnection):
    def _create_conn(self, **config):
        from kafka import KafkaProducer
        return KafkaProducer(**config)


dbcs = {"kafka": KafkaPoolConnection}

pool = Pool(bootstrap_servers="10.57.31.22:9092,10.57.31.23:9092,10.57.31.24:9092")


def test(conn):
        ts = int(time.time() * 1000)
        conn.send(topic="jyztest", value=str(i),timestamp_ms=ts)





if __name__ == "__main__":
    i = 0
    while True:
        conn = pool.get()
        test(conn)
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + str(i % 6)
        print conn
        i += 1
        time.sleep(1)
