import protocol_constants as pc
import json
import time
from thread import *
from pymongo import MongoClient
import hashlib

import networkx as nx

import signal
import sys


constants = {
	'reorder_period': 1200, # 20 mins
	'connection_lost_period': 30, # 30s
}

class CrawlMaster:
	clients = {}

	server_status = pc.STATUS_RUNNING

	last_rereoder_time = time.time()

	is_reordering = False

	def __init__(self, mongo_host='localhost'):
		self.mongo_client = MongoClient(mongo_host, 27017)
		self.db = self.mongo_client.spider


	def reorder_queue(self):
		g = nx.DiGraph()
		cursor = self.db.urlpr.find()
		for site in cursor:
			url = site['url']
			links = site['links']
			g.add_node(url)
			for link in links:
				g.add_edge(url, link)
		pageranks = nx.pagerank(g, 0.9)
		for url, pr in pageranks.iteritems():
			record = {'pr': pr}
			self.db.mfw.update_one({'_id': hashlib.md5(url).hexdigest()}, {'$set': record}, upsert=False)


crawl_master = CrawlMaster()
crawl_master.reorder_queue()