#!/usr/python/bin

import json
import os

from aliyunsdkcore.client import AcsClient


def GetAliyunClient(akskconfig):
    with open(akskconfig, 'r') as fp:
        alibaba_cloud_config = json.loads(fp.read())

    client = AcsClient(
        alibaba_cloud_config.get('AccessKeyID'),
        alibaba_cloud_config.get('AccessKeySecret'),
        alibaba_cloud_config.get('RegionID')
    );
    return client
