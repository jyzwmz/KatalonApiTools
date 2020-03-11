#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.dom.minidom as Dom
import xml.dom.minidom
import json
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf8')

csvfile = file('/Users/jinyongzhe/Downloads/农行POC/output/full.csv', 'wb')
csvfile.write(u'\ufeff'.encode('utf8'))
writer = csv.writer(csvfile)
writer.writerow(['success', 'reason_code', 'ignoreReq'])
dom = xml.dom.minidom.parse("/Users/jinyongzhe/Downloads/农行POC/output/full.xml")
root = dom.documentElement
for sampleCount in root.getElementsByTagName('httpSample'):
    print sampleCount.getElementsByTagName('responseData')[0].childNodes[0].data
    jsonSample = json.loads(sampleCount.getElementsByTagName('responseData')[0].childNodes[0].data)
    #print jsonSample
    #print jsonSample["success"]
    data = [(jsonSample["success"],jsonSample["reason_code"],jsonSample["ignoreReq"])]
    writer.writerows(data)
csvfile.close()

