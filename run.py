#!/usr/bin/env python
# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
import json
import time
import sys
from datetime import datetime
from datetime import timedelta

esAddress = ''
es = Elasticsearch([esAddress])
ipList_old = []
ipList_new = []
searchDoc = """{"query":{"filtered":{"query":{"query_string":{"query":"clienthost2:c.nishuoa.com","analyze_wildcard":true}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":1449479998710,"lte":1449480898710}}}],"must_not":[]}}}},"size":0,"aggs":{"1":{"terms":{"field":"clienthost.raw","size":150000,"order":{"_count":"desc"}}}}}"""


# Convert to UNIX
def datetime_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


# Get JSON data
def getIPListToFile(start, over):
    gte = datetime_timestamp(start)
    lte = datetime_timestamp(over)
    indexDoc = "logstash-" + start.strftime("%Y") + "." + start.strftime("%m") + "." + start.strftime("%d")
    print indexDoc
    res = es.search(
        index=indexDoc,
        doc_type='IISLog',
        body=searchDoc.replace('1449479998710', str(gte) + '000').replace('1449480898710', str(lte) + '000')
    )

    with open(str(start), 'wt') as f:
        f.write(json.dumps(res))


if __name__ == '__main__':
    argList = []
    for arg in sys.argv:
        argList.append(arg)
    st = datetime.strptime(argList[1], '%Y-%m-%d')
    ot = st + timedelta(hours=23, minutes=59, seconds=59)
    getIPListToFile(st, ot)
    st1 = st - timedelta(days=1)
    ot1 = ot - timedelta(days=1)
    getIPListToFile(st1, ot1)

    with open(str(st), 'rt') as f:
        data_new = json.load(f)

    with open(str(st1), 'rt') as f:
        data_old = json.load(f)

    output = data_new['aggregations']['1']['buckets']
    for buckets in output:
        ipList_new.append(buckets['key'])

    output = data_old['aggregations']['1']['buckets']
    for buckets in output:
        ipList_old.append(buckets['key'])

    comparisonIPList = set(ipList_new) - set(ipList_old)

    with open(argList[1] + "_No_repeat_IP_list.txt", 'wt') as f:
        f.write("No repeat IP is :" + str(len(comparisonIPList)))
        f.write("\n\n")
        f.write("List:\n\n")
        for ii in comparisonIPList:
            f.write(ii + "\n")
