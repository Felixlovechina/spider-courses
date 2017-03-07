from pymongo import MongoClient


class ItemCompare():

    def __init__(self):
        self.client = MongoClient('', 27017) if client is None else client