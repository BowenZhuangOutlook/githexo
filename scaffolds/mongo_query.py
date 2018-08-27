#!/usr/bin/python
# -*- coding:utf-8 -*-  
'''
	get mongodb slow query 
'''
__author__ = 'bowenz'

import datetime
from pymongo import MongoClient
from bson.son import SON
import codecs
import json
from bson import json_util
import hashlib


def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)


def get_md5(data):
    data_md5 = hashlib.md5(json.dumps(data, sort_keys=True)).hexdigest()
    return data_md5


nowtime = datetime.datetime.now()
dbhost = "mongodb://sjprmongodb01.ehealthinsurance.com/?ssl=true&ssl_ca_certs=ca.cer"
dbport = 27017
dbuser = "root"
dbpass = "xxxx"
client = MongoClient(dbhost, dbport)
client['admin'].authenticate(dbuser, dbpass)
dbnames = client.list_databases()
for dbname in dbnames:
    if dbname["name"] in ("admin", "local"):
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
    if maxtime < nowtime - datetime.timedelta(days=7):
        continue
    gttime = nowtime - datetime.timedelta(days=7)
    pipeline = [
        {"$match": {"ts": {"$gt": gttime}}},
        {"$group": {"_id": "$ns", "cnt": {"$sum": 1}}},
        {"$sort": SON([("cnt", -1)])}
    ]
    nss = collection.aggregate(pipeline)
    print('=======================================')
    print('Database Name is : %s ' % dbname["name"])
    print('system profile collection count : %d ' % cnt)
    print(maxrow["maxtime"])
    SQLQueue = {}
    for ns in nss:
        print('performance collection name is %s , count is %s ' % (ns["_id"], ns["cnt"]))
        performanceSQLs = collection.find({"ns": ns["_id"], "ts": {"$gt": gttime}}).sort([("ts", -1)])
        for performanceSQL in performanceSQLs:
            performanceSQLJson = json.dumps(performanceSQL, encoding='latin1', default=json_util.default,
                                            sort_keys=True, indent=4)
            dictSQL = json.loads(performanceSQLJson)
            keys = []
            get_keys(dictSQL, keys)
            keys.sort()
            SQLQueue[ns["_id"] + "." + get_md5(keys)] = performanceSQLJson

    for key in SQLQueue.keys():
        with codecs.open("./mgsql/" + key + ".json", 'a', 'utf-8') as outf:
            outf.write(SQLQueue[key])

"""
# performanceSQL = collection.find({"ns": ns["_id"]}).sort([("ts", -1)]).limit(1).next()
# with codecs.open("./mgsql/" + ns["_id"] + ".json", 'a', 'utf-8') as outf:
#     json.dump(performanceSQL, outf, ensure_ascii=False, default=json_util.default, sort_keys=True, indent=4, )

db.system.profile.aggregate( [{$group:{_id:null,maxvalue:{$max:"$ts"}}}])
db.system.profile.aggregate( [ {$match:{"ts":{"$gt":xxx}} },{$group:{_id:"$ns", cnt:{$sum:1}}}] )
db.system.profile.aggregate( [ {$group:{_id:"$ns", cnt:{$sum:1}}}] )
db.system.profile.find({"ns": "mapsdb.medicareSearch"}).sort({"ts": -1}).limit(1)
"""
