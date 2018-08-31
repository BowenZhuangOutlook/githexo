#!/usr/bin/python
# -*- coding:utf-8 -*-  
import datetime
import codecs
import json
import base64
import hashlib
import os, sys
from bson.son import SON
from bson import json_util
from pymongo import MongoClient
from mg_config import *

log = "%s/%s/summary.log" % (mg_slow_query_config["output"], datetime.datetime.now().strftime("%Y%m%d"))
sys.stdout = Logger(log)
print("======================%s=============================" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)


def get_md5(data):
    data_md5 = hashlib.md5(json.dumps(data, sort_keys=True)).hexdigest()
    return data_md5


def get_hist(output):
    hist = set()
    for root, dirs, files in os.walk(output):
        for f in files:
            if os.path.splitext(f)[1] == '.json':
                hist.add(os.path.splitext(f)[0])
    return hist


def main():
    isEmail = False
    nowtime = datetime.datetime.now()
    client = MongoClient(base_config["dbhost"], base_config["dbport"])
    client['admin'].authenticate(base_config["dbuser"], base64.decodestring(base_config["dbpass"]))
    dbnames = client.list_databases()
    for dbname in dbnames:
        if dbname["name"] in mg_slow_query_config["slowdbname"]:
            continue
        db = client[dbname["name"]]
        collection = db['system.profile']
        cnt = collection.count()
        if cnt == 0:
            continue
        pipeline = [
            {"$group": {"_id": None, "maxtime": {"$max": "$ts"}}}
        ]
        maxrow = collection.aggregate(pipeline).next()
        maxtime = maxrow["maxtime"]
        if maxtime < mg_slow_query_config["gttime"]:
            continue
        gttime = mg_slow_query_config["gttime"]
        lttime = mg_slow_query_config["lttime"]
        pipeline = [
            {"$match": {"ts": {"$gt": gttime, "$lt": lttime}, "millis": {"$gt": mg_slow_query_config["slowms"]}}},
            {"$group": {"_id": "$ns", "cnt": {"$sum": 1}}},
            {"$sort": SON([("cnt", -1)])}
        ]
        nss = collection.aggregate(pipeline)
        print('=======================================')
        print('Database Name is : %s' % dbname["name"])
        print('system profile collection count : %d ' % cnt)
        print('mongodb slow query range between %s to %s' % (gttime, lttime))
        SQLQueue = {}
        CntQueue = {}
        HistQueue = get_hist(mg_slow_query_config["output"])
        for ns in nss:
            print('performance collection name is %s , count is %s ' % (ns["_id"], ns["cnt"]))
            performanceSQLs = collection.find({"ns": ns["_id"], "ts": {"$gt": gttime, "$lt": lttime},
                                               "millis": {"$gt": mg_slow_query_config["slowms"]}}).sort([("ts", -1)])
            for performanceSQL in performanceSQLs:
                performanceSQLJson = json.dumps(performanceSQL, encoding='latin1', default=json_util.default,
                                                sort_keys=True, indent=4)
                dictSQL = json.loads(performanceSQLJson)
                tmpmillis = dictSQL["millis"]
                keys = []
                get_keys(dictSQL, keys)
                keys.sort()
                queueKey = ns["_id"] + "-" + get_md5(keys)
                CntQueue[queueKey] = CntQueue.get(queueKey, 0) + 1
                if SQLQueue.has_key(queueKey):
                    performanceSQLJson = (
                        SQLQueue[queueKey] if tmpmillis >= dictSQL["millis"] else performanceSQLJson)
                SQLQueue[queueKey] = performanceSQLJson

        for key in SQLQueue.keys():
            if CntQueue[key] <= mg_slow_query_config["slowcnt"] or \
                            key.split("-")[0] in mg_slow_query_config["slowcollection"]:
                print("performance collection name %s will be ignored, this's count is %s " % (key, CntQueue[key]))
                continue
            if key in HistQueue:
                print(
                    "performance collection name %s will be ignored, it has appeared in the past ,this's count is %s " % (
                        key, CntQueue[key]))
                continue
            print('performance collection name SQL_ID is %s, count is %s' % (key, CntQueue[key]))
            output = "%s/%s/" % (mg_slow_query_config["output"], datetime.datetime.now().strftime("%Y%m%d"))
            if not os.path.exists(output):
                os.makedirs(output)
            with codecs.open(output + key + ".json", 'a', 'utf-8') as outf:
                outf.write(SQLQueue[key])
            isEmail=True

    if isEmail:
        send_mail(mg_slow_query_config["Eheader"], mg_slow_query_config["ECC"], mg_slow_query_config["ETO"], log)


if __name__ == '__main__':
    main()
