#!/usr/bin/python
# coding:utf8


from AliyunBaseHelper import GetAliyunClient
import datetime
import json
from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkrds.request.v20140815 import (DescribeBackupsRequest,
                                            DescribeBinlogFilesRequest,
                                            DescribeDBInstancesRequest)


# 设置获取db实例列表的request
def SetRdsInstancesRequest(pagesize):
    rdsrequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    rdsrequest.set_PageSize(pagesize)
    return rdsrequest

# 设置获取db备份列表的request
def SetRdsbakRequest(RDSInstanse, StartTime, EndTime):
    '''
    rdsbkbody = {
    "Action": "DescribeBackups",
    "DBInstanceId": rdsrep['Items']['DBInstance'][]['DBInstanceId'],
    "BackupStatus": "Success",
    "StartTime": StartTime,
    "EndTime": EndTime,
    "PageSize": 10,
    "PageNumber": 30
    }
    '''
    rdsbkrequest = DescribeBackupsRequest.DescribeBackupsRequest()
    rdsbkrequest.add_query_param("DBInstanceId", RDSInstanse)
    rdsbkrequest.add_query_param("StartTime", StartTime)
    rdsbkrequest.add_query_param("EndTime", EndTime)
    return rdsbkrequest

# 设置获取binlog日志文件
def SetRdsbinlogRequest(DBInstanceId, StartTime, EndTime):
    try:
        rdsbinlogrequest = DescribeBinlogFilesRequest.DescribeBinlogFilesRequest()
        rdsbinlogrequest.set_DBInstanceId(DBInstanceId)
        rdsbinlogrequest.set_StartTime(StartTime)
        rdsbinlogrequest.set_EndTime(EndTime)
        return rdsbinlogrequest
    except Exception as e:
        print e

# 根据request,获取response
def GetResponse(client, request):
    try:
        rdsresponse = client.do_action_with_exception(request)
        return rdsresponse
    except ServerException as e:
        print e.get_http_status()
        print e.get_error_code()
        print e.get_error_msg()

if __name__ == '__main__':
    pass
