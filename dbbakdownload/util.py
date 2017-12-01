#!/usr/bin/python
# -*- coding: utf8 -*-
import re
import urllib
import os
import chardet
def get_bak_filename(url):
    re1='.*?'	# Non-greedy match on filler
    re2='(hins)'	# Word 1
    re3='(\\d+)'	# Integer Number 1
    re4='(_)'	# Any Single Character 1
    re5='(data)'	# Word 2
    re6='(_)'	# Any Single Character 2
    re7='(\\d+)'	# Integer Number 2
    re8='(\\.)'	# Any Single Character 3
    re9='(tar\\.gz)'	# Fully Qualified Domain Name 1

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9,re.IGNORECASE|re.DOTALL)
    m = rg.search(url)

    if m:
        word1=m.group(1)
        int1=m.group(2)
        c1=m.group(3)
        word2=m.group(4)
        c2=m.group(5)
        int2=m.group(6)
        c3=m.group(7)
        fqdn1=m.group(8)
        return word1+int1+c1+word2+c2+int2+c3+fqdn1


def get_binlog_filename(url):
    re1='.*?'	# Non-greedy match on filler
    re2='(?:[a-z][a-z\\.\\d\\-]+)\\.(?:[a-z][a-z\\-]+)(?![\\w\\.])'	# Uninteresting: fqdn
    re3='.*?'	# Non-greedy match on filler
    re4='((?:[a-z][a-z\\.\\d\\-]+)\\.(?:[a-z][a-z\\-]+))(?![\\w\\.])'	# Fully Qualified Domain Name 1

    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    m = rg.search(url)
    if m:
        fqdn1=m.group(1)
        return fqdn1


def download_file(filepath, url, filename):
    filename = str(filename)
    filename = os.path.join(filepath,filename)
    print 'Starting Download bak of %s' % filepath
    urllib.urlretrieve(url, filename)
    print 'download %s ' %filename ,'Successful'
    return str(filename)

def datetime_cmp(date1, date2):
    t_st1 = time.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    t_st2 = time.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    timestamp1 = time.mktime(t_st1)
    timestamp2 = time.mktime(t_st2)

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%s'%str(c),'%.f%%' % per


def mkdir(path):
    path=path.strip()
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print 'Folder' + path + 'created successful'

if __name__ == "__main__":
    get_binlog_filename('http://rdslog-bjc-v2.oss-cn-beijing-c.aliyuncs.com/custins4512149/hostins3263493/mysql-bin.000295.tar?OSSAccessKeyId=LTAITfQ7krsrEwRn&Expires=1512183678&Signature=jvEOHL9eWsrOC4p+hrm6gHuDswE=')