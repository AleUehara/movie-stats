from pymongo import Connection, MongoClient

class MongoDBConnection():
    def __init__(self):
        client = MongoClient('localhost', 27021)
        db = client.test_database
        self.mongo_collection = db.movie_collection

    def insert_collection(self, jsonfile):
        insert_id = self.mongo_collection.insert(jsonfile)

    def select_one(self):
        print self.mongo_collection.find_one()

    def count(self):
        print self.mongo_collection.count()

    def all_rates(self):
    	pass



#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    MongoDBConnection()