#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import uuid
import random
from kafka import KafkaProducer
from faker import Faker
from locust import Locust, TaskSet, events, task

def get_time():
    time.sleep(random.random())
    return time.time()

def get_random_number(low, high):
    time.sleep(random.random())
    return random.randint(low, high)

class KafkaClient(object):

    def __init__(self):
        #self.host = kfk_url
        self.producer = KafkaProducer(bootstrap_servers='10.57.31.134:9092')
        self.fake=Faker("zh-CN")

    def kafka_send(self):
        try:
            start_time = time.time()
            ts = int(time.time() * 1000)
            vContent = self.fake.name()+','+self.fake.credit_card_number()+','+self.fake.phone_number()+','+ \
                       self.fake.ssn()+','+self.fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
            self.producer.send(topic="jyztest",value=vContent,key=uuid.uuid1(),timestamp_ms=ts)
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="kafkaProducer",name='UserInfo', response_time = total_time, response_length = 0)
        except Exception as error:
            print(error)
            events.request_failure.fire(request_type="kafkaProducer",name='UserInfo', response_time = total_time, exception = error)

#class KafkaLocust(Locust):
    #def __init__(self, *args, **kwargs):
        #super(KafkaClient, self).__init__(*args, **kwargs)
        #self.client = KafkaClient()

class KafkaTask(TaskSet):
    """压测任务"""
    def on_start():
        #all_locusts_spawned.wait()
        pass

    @task
    def GenerateUserInfo(self):
        self.client.kafka_send()

class WebsiteUser(Locust):
    task_set = KafkaTask
    min_wait = 5000
    max_wait = 9000