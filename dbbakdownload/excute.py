#!/usr/bin/python
# coding:utf8

import datetime
import json
import os
import Queue
import sys
import threading

from AliyunBaseHelper import GetAliyunClient
from AliyunOssHelper import GetBucket, GetOssAuth, PutObjectFromFile
from AliyunRdsHelper import (GetResponse, SetRdsbakRequest,
                             SetRdsbinlogRequest, SetRdsInstancesRequest)
from Thread import startThread
from util import get_bak_filename, get_binlog_filename, mkdir

akskconfig = 'aksk.ini'
dirpath = '/'
ossendpoint = 'oss-cn-beijing.aliyuncs.com'
bucketname = 'gd-db-bak'



def setup():
    # 创建AcsClient实例
    client = GetAliyunClient(akskconfig)
    # 创建 request，并设置参数
    rdsrequest = SetRdsInstancesRequest(20)
    return client, rdsrequest

def main():
    client, rdsrequest = setup()
    # getresponse
    nowtime = datetime.datetime.now()
    starttime = nowtime
    starttime -= datetime.timedelta(days=7)
    StartTime = starttime.strftime('%Y-%m-%dT%H:%MZ')
    EndTime = nowtime.strftime('%Y-%m-%dT%H:%MZ')
    EndTime2 = nowtime.strftime('%Y-%m-%dT%H:%M:%SZ')
    dirpath = os.getcwd()
    newfolder = os.path.join(dirpath, EndTime)
    mkdir(newfolder)
    RDSInstanselist = [''] # rds实例id
    for i in RDSInstanselist:
        newfolder2 = os.path.join(newfolder, i)
        mkdir(newfolder2)
    RDSBakUrllist = []
    for RDSInstanse in RDSInstanselist:
        RDSBak = {}
        rdsbakrequest = SetRdsbakRequest(RDSInstanse, StartTime, EndTime)
        rdsbkresponse = GetResponse(client, rdsbakrequest)
        bkresp = json.loads(rdsbkresponse)
        url = bkresp['Items']['Backup'][0]['BackupDownloadURL']
        BackupEndTime = bkresp['Items']['Backup'][0]['BackupEndTime']
        BackupStartTime = bkresp['Items']['Backup'][0]['BackupStartTime']
        filename = get_bak_filename(url)
        RDSBak.setdefault('RDSInstanse', RDSInstanse)
        bakdownloadurldict = {}
        bakdownloadurldict.setdefault(get_bak_filename(url),url)
        RDSBak.setdefault('BackupEndTime', BackupEndTime)
        RDSBak.setdefault('BackupStartTime', BackupStartTime)
        rdsbinlogrequest = SetRdsbinlogRequest(RDSInstanse, BackupEndTime, EndTime2)
        rdsbinlogresponse = GetResponse(client, rdsbinlogrequest)
        binlogresp = json.loads(rdsbinlogresponse)
        TotalRecordCount = binlogresp['TotalRecordCount']
        for i in range(TotalRecordCount):
            bakdownloadurldict.setdefault(get_binlog_filename(binlogresp['Items']['BinLogFile'][i]['DownloadLink']),binlogresp['Items']['BinLogFile'][i]['DownloadLink'])
        RDSBak.setdefault('bakdownloadurldict', bakdownloadurldict)
        RDSBakUrllist.append(RDSBak)
    for i in RDSBakUrllist:
        print i
    auth = GetOssAuth('aksk.ini')
    bucket = GetBucket(auth, '', '') # ossendpoint , bucketname
    startThread(bucket, RDSBakUrllist, newfolder, EndTime)

if __name__ == "__main__":
    main()
