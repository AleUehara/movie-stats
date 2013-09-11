from pymongo import Connection, MongoClient
from bson.objectid import ObjectId
from bson.son import SON
from bson.code import Code

class MongoDBConnection():
    def __init__(self):
        client = MongoClient('localhost', 27021)
        self.db = client.movies
        self.collection = self.db.movie_collection

    def insert_collection(self, imdbid, jsonfile):
        self.drop_collection()
        self.imdbid = {"userid" : imdbid}
        self.collection.insert(  {"userid" : imdbid, "movies" : jsonfile} )
        
        

    def drop_collection(self):
        self.collection.drop()

    def select_one(self):
        print self.collection.find_one({"userid" : "45031138"})

    def select_all(self):
        print self.collection.find()

    def count(self):
        print self.collection.count()

    def all_rates(self):
        pass

    def test(self):
        result = self.collection.aggregate( [       {"$match" : {"userid" : "45031138"}, "$match": {"movies" : 1}},
                                                    #{"$match": {"movies" : 1}}
                                                    #{"$group":{"_id":"$Year", 
                                                    #          "avg": {"$avg": "$rated"}
                                                    #          }
                                                    #},
                                                    #{"$sort": SON([("_id", -1), ("avg", -1)])}
                                            ]
                                          )
        print result


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












class IMDB_Data():
  def __init__(self):
    self.values = []

  def execute_aggregate_list(self):
        #print self.query
        #print self.collection
        result = self.collection.aggregate( self.query )
        #print "INICIO"
        #print self.columns
        self.create_return(result, self.columns)

  
  def create_return(self, result, columns_name):
    for i in result.get("result"):
        movielist = []
        for column_name in columns_name:
            print column_name
          
            key = column_name.keys()[0]
            if column_name.values()[0] == "str":
              movielist.append(str(i.get(key)))
            elif column_name.values()[0] == "int":
              movielist.append(int(i.get(key)))
        #print "=============="
        
        self.values.append(movielist)

        print self.values
    
        





class IMDBAggregation(IMDB_Data):
  def __init__(self):
     IMDB_Data.__init__(self)
     self.execute_aggregate_list()



class TopDirectorsRating(IMDBAggregation):
  def __init__(self, movie_collection):
     self.collection = movie_collection
     self.title = "Top Directors Rating"
     self.query = [ #{"$userid" : "45031138"},{"$movies": 1},
                    {"$group":{"_id":"$Directors", 
                               "average": {"$avg": "$rated"},
                               "count": {"$sum": 1}
                              }
                    },
                    {"$sort": SON([("average", -1), ("_id", -1)])},
                    {"$limit" : 5}
                  ]
     self.columns = [{"_id" :"str"}, {"average" : "int"}]
     IMDBAggregation.__init__(self)


class MoviesByYear(IMDBAggregation):
  def __init__(self, movie_collection):
     self.collection = movie_collection
     self.title = "Movies By Year"
     self.query =  [
                    {"$group":{"_id":"$Year", 
                              "count": {"$sum": 1}
                              }
                    },
                    {"$sort": SON([("_id", -1), ("count", -1)])}
                   ]
     self.columns = [{"_id" :"str"}, {"count" : "int"}]
     IMDBAggregation.__init__(self)





class TotalMinutesWatched(IMDBAggregation):
  def __init__(self, movie_collection):
      self.collection = movie_collection
      self.title = "Total Minutes Watched"
      self.query = [
                  {"$group":{"_id":"", 
                             "sum_runtime": {"$sum": "$Runtime (mins)"}
                            }
                  }
                 ]
      self.columns = [{"sum_runtime" : "int"}]
      IMDBAggregation.__init__(self)

  def create_return(self, result, first_column_name, second_column_name=""):
        #minutes_watched = result.get("result")[0].get("sum_runtime")
        minutes_watched = result.get("result")[0].get(first_column_name)
        print '--------------------------'
        print minutes_watched
        #return str(minutes_watched / 60) + " hours or " + str(minutes_watched) + " minutes"
        return "teste"

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    MongoDBConnection()