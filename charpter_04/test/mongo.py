import mysql.connector
import httplib
import hashlib
import time 
from datetime import datetime
from datetime import timedelta

import redis
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING


class MongoRedisUrlManager:

    def __init__(self, sever_ip='localhost', client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # if a client object is not passed 
        # then try connecting to mongodb at the default localhost port 
        self.client = MongoClient(sever_ip, 27017) if client is None else client
        self.redis_client = redis.StrictRedis(host=sever_ip, port=6379, db=0) 
        #create collection to store cached webpages,
        # which is the equivalent of a table in a relational database
        self.db = self.client.spider

        # create index if db is empty
        if self.db.mfw.count() is 0:
            self.db.mfw.create_index([("status", ASCENDING), 
                ("pr", DESCENDING)])


    def dequeueUrl(self):
        record = self.db.mfw.find_one_and_update(
            { 'status': 'new'}, 
            { '$set': { 'status' : 'downloading'} }, 
                upsert=False, 
                sort=[('pr', DESCENDING)], # sort by pr in descending 
                returnNewDocument= False
        )
        if record:
            return record
        else:
            return None

    def enqueuUrl(self, url, status, depth):
        self.db.mfw.insert({
            '_id': hashlib.md5(url).hexdigest(), 
            'url': url, 
            'status': status, 
            'queue_time': datetime.utcnow(), 
            'depth': depth,
            'pr': 0.99 - float(depth)/20
        })

    def finishUrl(self, url):
        record = {'status': 'done', 'done_time': datetime.utcnow()}
        self.db.mfw.update({'_id': hashlib.md5(url).hexdigest()}, {'$set': record}, upsert=False)

    def set_url_links(self, url, links):
        self.db.urlpr.insert({
            '_id': hashlib.md5(url).hexdigest(), 
            'url': url, 
            'links': links
        })

    def clear(self):
        self.db.mfw.drop()


client = MongoRedisUrlManager()

client.enqueuUrl('mfw', 'new', 0)
client.enqueuUrl('baidu', 'new', 0)
client.enqueuUrl('sina', 'new', 0)
client.enqueuUrl('ali', 'new', 0)
client.enqueuUrl('taobao', 'new', 0)
client.enqueuUrl('leshi', 'new', 0)

client.set_url_links('mfw', ('baidu', 'sina', '163', 'mfw'))
client.set_url_links('baidu', ('baidu', 'sina', '163', 'mfw'))
client.set_url_links('sina', ('baidu', '163', 'ali', 'mfw'))
client.set_url_links('ali', ('baidu', 'qunar', 'ali', 'mfw'))
client.set_url_links('taobao', ('baidu', 'wanmei', '163', '163'))
client.set_url_links('leshi', ('baidu', 'qunar', 'ali', 'mfw'))