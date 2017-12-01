#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os

import oss2


def GetOssAuth(akskconfig):
    with open(akskconfig ) as fp:
        alibaba_cloud_config = json.loads(fp.read())  
    auth = oss2.Auth(alibaba_cloud_config.get('AccessKeyID'), alibaba_cloud_config.get('AccessKeySecret'))
    return auth

def GetBucket(auth, ossendpoint, bucketname):
    bucket = oss2.Bucket(auth, ossendpoint, bucketname)
    return bucket

def PutObjectFromFile(bucket, key, filename):
    print filename
    print key
    try:
        bucket.put_object_from_file(key, filename)
    except Exception as e:
        print e



if __name__ == "__main__":
    pass
