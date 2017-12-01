#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import Queue
import threading
import time
from util import download_file
from AliyunOssHelper import PutObjectFromFile

class myThread (threading.Thread):
    def __init__(self, threadID, q, dirpath, bucket, newdate):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dirpath = dirpath
        self.q = q
        self.bucket = bucket
        self.newdate = newdate
    def run (self):
        queueLock.acquire()
        print '-' * 10 , 'Start threadID: %d ' % self.threadID, '-' * 10 , '\n'
        queueLock.release()
        if not workQueue.empty():
            queueLock.acquire()
            data = self.q.get()
            downloadpath = os.path.join(self.dirpath, data['RDSInstanse'])
            queueLock.release()
            for download in data['bakdownloadurldict'].items():
                objectpath = download_file(downloadpath, str(download[1]), str(download[0]))
                putobjectpath = os.path.join(str(self.newdate), os.path.join(str(data['RDSInstanse']), str(download[0])))
                print putobjectpath
                PutObjectFromFile(self.bucket , putobjectpath, objectpath)
                print 'put %s to oss successful' % putobjectpath
        else:
            print '-' * 10 , 'Start threadID: %d ' % self.threadID, '-' * 10 , '\n'


queueLock = threading.Lock()
workQueue = Queue.Queue(10)
def startThread(bucket, RDSBakUrllist, newfolder, newdate):

    threads = []
    threadID = 1
    for RDSBak in RDSBakUrllist:
        workQueue.put(RDSBak)
    for RDSBakUrl in RDSBakUrllist:
       thread = myThread(threadID, workQueue, newfolder, bucket, newdate)
       thread.start()
       threads.append(thread)
       threadID += 1

    for t in threads:
        t.join()
    
