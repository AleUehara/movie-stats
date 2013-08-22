from pymongo import Connection, MongoClient
from bson.son import SON
from bson.code import Code

class MongoDBConnection():
    def __init__(self):
        client = MongoClient('localhost', 27021)
        self.db = client.movies
        self.collection = self.db.movie_collection

    def insert_collection(self, jsonfile):
        self.collection.drop()
        insert_id = self.collection.insert(jsonfile)

    def select_one(self):
        print self.collection.find_one()

    def count(self):
        print self.collection.count()

    def all_rates(self):
        pass

    def movies_rates_by_year(self):
        result = self.collection.aggregate( [
                                                    {"$group":{"_id":"$Year", 
                                                              "avg": {"$avg": "$rated"}
                                                              }
                                                    },
                                                    {"$sort": SON([("_id", -1), ("avg", -1)])}
                                                   ]
                                                 )
        returnlist = []
        for i in result.get("result"):
            movielist = [i.get("_id"), i.get("avg")]
            returnlist.append(movielist)
        print returnlist
        return returnlist

    def movies_by_directors(self):
        result = self.collection.aggregate( [
                                                    {"$group":{"_id":"$Directors", 
                                                              "count": {"$sum": 1}
                                                              }
                                                    },
                                                    {"$sort": SON([("count", -1)])},
                                                   ]
                                                 )
        for i in result.get("result"):
            print i.get("_id") +"-->"+ str(i.get("count"))
        print "-------------------"

    def top_directors_watched(self, top_number):
        result = self.collection.aggregate( [
                                                    {"$group":{"_id":"$Directors", 
                                                              "count": {"$sum": 1}
                                                              }
                                                    },
                                                    {"$sort": SON([("count", -1)])},
                                                    {"$limit" : top_number}
                                                   ]
                                                 )
        #for i in result.get("result"):
        #    print i.get("_id") +"-->"+ str(i.get("count"))

        returnlist = []
        for i in result.get("result"):
            movielist = [str(i.get("_id")), i.get("count")]
            returnlist.append(movielist)
        return returnlist



    def movies_by_year(self):
        for i in aggregation.get("result"):
            print str(i.get("total")) +"-->"+ i.get("_id")


        result1 = self.collection.aggregate( [
                                                    {"$group":{"_id":"$Year", 
                                                              "count": {"$sum": 1}
                                                              }
                                                    },
                                                    {"$sort": SON([("_id", -1), ("count", -1)])}
                                                   ]
                                                 )
        for i in result1.get("result"):
            print i.get("_id") +"-->"+ str(i.get("count"))


    def total_minutes_watched(self):
        result = self.collection.aggregate( [
                                                    {"$group":{"_id":"", 
                                                              "sum_runtime": {"$sum": "$Runtime (mins)"}
                                                              }
                                                    }
                                                   ]
                                                 )
        minutes_watched = result.get("result")[0].get("sum_runtime")
        print str(minutes_watched / 60) + " hours or " + str(minutes_watched) + " minutes"

class DirectorsRating():
  def __init__(self, movie_collection):
     self.collection = movie_collection
     self.title = "Top Directors Rating"
     
  def find(self):
        result = self.collection.aggregate( [
                                                    {"$group":{"_id":"$Directors", 
                                                              "average": {"$avg": "$rated"},
                                                              "count": {"$sum": 1}
                                                              }
                                                    },
                                                    {"$sort": SON([("average", -1), ("_id", -1)])},
                                                    {"$limit" : 5}
                                                   ]
                                                 )
        #for i in result.get("result"):
        #    print i.get("_id") +"-->"+ str(i.get("average")) +"-->"+str(i.get("count")) + "\n"

        
        returnlist = []
        for i in result.get("result"):
            movielist = [str(i.get("_id")), i.get("average")]
            returnlist.append(movielist)
        
        return returnlist


#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    MongoDBConnection()