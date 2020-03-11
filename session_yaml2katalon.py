#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import urlparse
import xml.dom.minidom as Dom
import xml.dom.minidom
import urllib
import uuid
import sys
import os
import time
import json
import random
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def save(filename, contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()

strCaseName = 'Script'+str(int(time.time())*1000)+'.groovy'
print strCaseName
strCase = """import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import internal.GlobalVariable as GlobalVariable
import groovy.json.JsonSlurper as JsonSlurper
import static org.assertj.core.api.Assertions.*

response = WS.sendRequest(findTestObject('search_and_replace', [('tdToken') : GlobalVariable.token]))
println response.getResponseText()
// Verify the response
WS.verifyResponseStatusCode(response, 200)
assertThat(response.getResponseText()).contains("success","code","message")
if (new JsonSlurper().parseText(response.getResponseText()).code == 200)
assertThat(new JsonSlurper().parseText(response.getResponseText())).hasSize(4)"""
#print (strCase.replace('search_and_replace','_bridgeApi_license'))
#save('/Users/jinyongzhe/Downloads/file.groovy', strCase.replace('search_and_replace','_bridgeApi_license'))
strTC = """<?xml version="1.0" encoding="UTF-8"?>
<TestCaseEntity>
   <description></description>
   <name>search_and_replace_name</name>
   <tag></tag>
   <comment></comment>
   <testCaseGuid>search_and_replace_guid</testCaseGuid>
</TestCaseEntity>"""
#print strTC.replace('search_and_replace_name','_bridgeApi_license').replace('search_and_replace_guid','9b08e0d9-7b05-11e9-8c5b-241b7acc9556')
#tcPath = sys.argv[4] + 'Test Cases/' + 'license1.tc'
#print "%s" % tcPath
#print os.path.isfile("%s" % tcPath)
#sys.exit()

if len(sys.argv)<4:
    print('Usage: python yaml2katalon.py path/RECORD+date+PM-JMeter.yaml path+xxx.rs TemplateOutputPath CaseOutputPath')
    sys.exit()

#f = open('/Users/jinyongzhe/Downloads/'+'jinyz.yaml')
f = open(sys.argv[1])
x = yaml.load(f)
#print (sys.argv[1])
#print (sys.argv[2])
#print (sys.argv[3])
#print x
filepath, tmpfilename = os.path.split(sys.argv[1])
shotname, extension = os.path.splitext(tmpfilename)
#print (filepath+':'+shotname+':'+extension)
#print (shotname[:-7])


#print x['scenarios']['RECORD 05-14-19 2.51.52 PM']['requests'][0]['do']
#RECORD 05-14-19 2.51.52 PM-JMeter.yaml
#for data in x['scenarios']['RECORD 05-14-19 2.51.52 PM']['requests'][0]['do']:
for data in x['scenarios'][shotname[:-7]]['requests'][0]['do']:
    print (data)
print ('-------------start---------------')
#列表中嵌套字典,按键值url实现去重复
l4=[]
l4.append(x['scenarios'][shotname[:-7]]['requests'][0]['do'][0])
print x['scenarios'][shotname[:-7]]['requests'][0]['do'][0]
for dict in x['scenarios'][shotname[:-7]]['requests'][0]['do']:
    #print len(l4)
    k=0
    for item in l4:
        #print 'item'
        if dict['url'] != item['url']:
            k=k+1
            #continue
        else:
            break
        #print k,len(l4)
        if k == len(l4):
            #print (dict['label'])
            parsed_tuple = urlparse.urlparse(dict['label'])
            strA = parsed_tuple[2]
            #print (strA.replace('/','_'))
            dict['label']=strA.replace('/','_')
            #dict.setdefault('body', []).append()
            if (not dict.has_key('body')):
                dict['body'] = {}
            if ('paas' in dict['label']):
                l4.append(dict)
                #print 'panduan-pass'+dict['label']
                print dict
print (len(l4))
print ('-------------end---------------')
#第一条记录处理
parsed_tuple1 = urlparse.urlparse(l4[0]['label'])
#print (parsed_tuple1[2])
l4[0]['label']=parsed_tuple1[2].replace('/','_')
if (parsed_tuple1[2] == '/'):
    #print (parsed_tuple1[2])
    l4.pop(0)
if (not 'body' in l4[0].keys()):
    l4[0]['body']=''
    #print 'body='+l4[0]['body']

#url拼接body
for data in l4:
    if (not data['body'] is None):
        if (data['method'] == 'GET'):
            data['url'] = data['url'] + '?' + urllib.urlencode(data['body']).replace('&', ';')
        if (data['method'] == 'POST' and ('=' in data['url']) and ('?' in data['url'])):
            data['method'] = 'GET'
            data['url'] = data['url'].replace('&', ';')
        print ('panduan' + data['url'] + '---' + urllib.urlencode(data['body']).replace('&', ';') + '---' + data['method'])
    # print data
print (len(l4))

#print l4[1]['body']
#sys.exit()

#dom = xml.dom.minidom.parse('/Users/jinyongzhe/Downloads/'+'userLogin.rs')
dom = xml.dom.minidom.parse(sys.argv[2])
root = dom.documentElement
#print root.nodeName
#print(root.childNodes)
#print root.getElementsByTagName('httpHeaderProperties')[0].getElementsByTagName('value')[0].childNodes[0].data

file_name = root.getElementsByTagName('name')
guid_id = root.getElementsByTagName('elementGuidId')
requestMethod = root.getElementsByTagName('restRequestMethod')
restUrl = root.getElementsByTagName('restUrl')
bodyContent = root.getElementsByTagName('httpBodyContent')
bodyType = root.getElementsByTagName('httpBodyType')
headProperyValue=root.getElementsByTagName('httpHeaderProperties')[0].getElementsByTagName('value')

#dictPOST={'contentType': 'multipart/form-data', 'charset': 'UTF-8', 'parameters': '[{name: jobOutTables,value: 0,type: Text}]'}
#dictPOST = json.dumps(dictPOST)
#print dictPOST
#bodyContent[0].firstChild.data = POST_Str_Parms
#fileName = sys.argv[3] + data['label']+'.rs'
#print fileName
#file_name[0].firstChild.data = data['label']
#restUrl[0].firstChild.data = data['url']
#requestMethod[0].firstChild.data = data['method']
#bodyType[0].firstChild.data='form-data'
#print (data['url']+data['label']+str(guid_id[0].firstChild.data)+data['method'])
#with open(fileName, 'w') as fh:
   # dom.writexml(fh, encoding='UTF-8')
#sys.exit()

#生成.rs接口文件
for data in l4:
    #print (data)
    nTime = int(time.time())*1000+random.randint(0,999)
    fileName = sys.argv[3] + data['label']+'.rs'
    file_name[0].firstChild.data = data['label']
    guid_id[0].firstChild.data = uuid.uuid1()
    requestMethod[0].firstChild.data = data['method']
    #requestMethod[0].firstChild.data = 'GET'
    restUrl[0].firstChild.data = data['url']
    #print data['body'] + data['method'] + data['url']
    if (data['method'] == 'POST'):
        bodyType[0].firstChild.data = 'form-data'
        headProperyValue[0].firstChild.data = 'multipart/form-data'
        print data['method'] + data['url']+str(data['body'])
        #print type(data['body'])
        #if (type(data['body']) is str):
        #    data['body'] = '{'+data['body'].replace("=", ':')+'}'
        #    print 'string='+str(data['body'])
        tempList = []
        for key, value in data['body'].items():
            tempDict = {}
            # print (key+':'+value)
            tempDict['type'] = 'Text'
            tempDict['name'] = key
            if (value == ''):
                tempDict['value']='""'
            else:
                tempDict['value'] = '"'+value+'"'
            # print tempDict
            tempList.append(tempDict)
        strList = str(tempList).replace("\'", '')
        print strList
        bodyContent[0].firstChild.data = '{"charset": "UTF-8", "contentType": "multipart/form-data", "parameters": strListSearchReplace}'.replace('strListSearchReplace', strList)
    print (data['url']+data['label']+str(guid_id[0].firstChild.data)+data['method'])

    if (not os.path.exists(fileName)):
        with open(fileName, 'w') as fh:
            dom.writexml(fh, encoding='UTF-8')
    else:
        print fileName

    if ('_login1' == data['label']):
        print '========'
        print fileName
        dom1 = xml.dom.minidom.parse(fileName)
        root1 = dom1.documentElement
        headList1 = root1.getElementsByTagName('httpHeaderProperties')[2]
        root1.removeChild(headList1)
        print '========='
        if (not os.path.exists(fPath)):
            with open(fileName, 'w') as fh1:
                dom1.writexml(fh1, encoding='UTF-8')
        else:
            print fileName

    fPath = sys.argv[4] + 'Scripts/' + data['label'] + '/'
    tcPath = sys.argv[4] + 'Test Cases/'
    if (not os.path.exists(fPath)):
        #print "%s" % fPath
        os.mkdir("%s" % fPath)

    if (os.path.exists(fPath)):
        #print "%s" % fPath
        #print (strCase.replace('search_and_replace', '_bridgeApi_license'))
        save("%s" % fPath+'Script'+str(nTime)+'.groovy', strCase.replace('search_and_replace',data['label']))
    else:
        print "%s" % fPath + 'Script' + str(nTime) + '.groovy'

    if (os.path.exists("%s" % tcPath)):
        #print "%s" % tcPath+data['label']+'.tc'
        save("%s" % tcPath+data['label']+'.tc',strTC.replace('search_and_replace_name', data['label']).replace('search_and_replace_guid',str(guid_id[0].firstChild.data)))
    else:
        #print strTC.replace('search_and_replace_name', data['label']).replace('search_and_replace_guid',str(guid_id[0].firstChild.data))
        print "%s" % tcPath + data['label'] + '.tc'
print('写入.rs接口文件 OK!')

