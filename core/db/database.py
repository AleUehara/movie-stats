from pymongo import Connection, MongoClient
from bson.objectid import ObjectId
from bson.son import SON
from bson.code import Code
import datetime

class MongoDBConnection():
    def __init__(self):
        client = MongoClient('localhost', 27021, safe = True)
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



class IMDB_Data():
  def __init__(self):
    self.values = []

  def execute_aggregate_list(self):
        result = self.collection.aggregate( self.query )
        self.create_return(result, self.columns)

  
  def create_return(self, result, columns_name):
    self.__calculate_result(result, columns_name)

  def __calculate_result(self, result, columns_name):
    for i in result.get("result"):
        movielist = []
        for column_name in columns_name:
          
            key = column_name.keys()[0]
            
            '''
            if type(i.get(key)) == dict:
              #print i.get(key)
              for data in i.get(key).items():
                print data[1]
                movielist.append(str(data[1]))
                print datetime.datetime.strptime('2005', '%Y')
            '''
            #print i.get(key)
            #print type(i.get(key))
            if column_name.values()[0] == "str":
              movielist.append(str(i.get(key)))
            elif column_name.values()[0] == "int":
              movielist.append(int(i.get(key)))
            elif column_name.values()[0] == "float":
              movielist.append(round(float(i.get(key)),2))
            #elif column_name.values()[0] == "float":
        
        self.values.append(movielist)
        #datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        





class IMDBAggregation(IMDB_Data):
  def __init__(self):
     IMDB_Data.__init__(self)
     self.execute_aggregate_list()

class TopDirectorsRating(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     IMDBAggregation.__init__(self)

  def create_return(self, result, first_column_name):
    self.values.append(['Director', 'Number of Movies', 'Average'])
    for director in result.get('result'):
      newvalue = [director.get("_id").encode("utf-8"), director.get("count"), round(float(director.get("average")),2) ]
      self.values.append(newvalue)


class TopDirectorsBestRating(TopDirectorsRating):
  def __init__(self, movie_collection, imdbid):
     self.title = "Top 5 Directors Best Rating (more than 3 movies watched)"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    {"$group":{"_id":"$movies.Directors", 
                               "average": {"$avg": "$movies.rated"},
                               "count": {"$sum": 1}
                              }
                    },
                    { "$match": { "count": { "$gt": 3 } } },
                    {"$sort": SON([("average", -1), ("_id", -1)])},
                    {"$limit" : 5}
                  ]
     self.columns = [{"_id" :"str"}, {"average" : "int"}]
     TopDirectorsRating.__init__(self, movie_collection, imdbid)
  


class TopDirectorsWorseRating(TopDirectorsRating):
  def __init__(self, movie_collection, imdbid):
     self.title = "Top 5 Directors Worse Rating (more than 3 movies watched)"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    {"$group":{"_id":"$movies.Directors", 
                               "average": {"$avg": "$movies.rated"},
                               "count": {"$sum": 1}
                              }
                    },
                    { "$match": { "count": { "$gt": 3 } } },
                    {"$sort": SON([("average", 1), ("_id", -1)])},
                    {"$limit" : 5}
                  ]
     self.columns = [{"_id" :"str"}, {"average" : "int"}]
     TopDirectorsRating.__init__(self, movie_collection, imdbid)
  

class TopDirectorsWatched(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     self.title = "Top 10 Directors Watched"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    {"$group":{"_id":"$movies.Directors", 
                              "count": {"$sum": 1}
                              }
                    },
                    {"$sort": SON([("count", -1)])},
                    {"$limit" : 10}
                  ]
     self.columns = [{"_id" :"str"}, {"count" : "int"}]
     IMDBAggregation.__init__(self)


class TopDirectorsWatchedLast3Years(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     current_year = datetime.datetime.now().year
     this_year = str(current_year)
     previous_year = str(current_year - 1)
     last_previous_year = str(current_year - 2)

     self.title = "Top 5 Directors Watched on the last 3 years. (" +this_year + ", "+previous_year+ ", " +last_previous_year+")"
     self.query =  [
                    { "$match": {"userid" : imdbid}},
                    { "$unwind": '$movies' },
                    { "$match": {"$or" : [{'movies.Year': this_year}, 
                                          {'movies.Year': previous_year}, 
                                          {'movies.Year': last_previous_year}]}},
                    { "$group":{"_id"  : "$movies.Directors", 
                                "count": {"$sum": 1}
                               }
                    },
                    {"$sort": SON([("count", -1)])},
                    {"$limit" : 5}
                  ]

     self.columns = [{"_id" :"str"},  {"count" : "int"}]
     IMDBAggregation.__init__(self)


class BestMovies(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     self.title = "Best Movies - Rate: 10"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    { "$match": {'movies.rated': 10} } ,
                    { "$group":{"_id": {"title" : "$movies.Title", "year" : "$movies.Release Date (month/day/year)", "year2" : "$movies.Release Date (month/day/year)"} }                    },
                    {"$sort": SON([("_id.year", -1)])},
                   ]
     self.columns = [{"_id" :"str"}]
     IMDBAggregation.__init__(self)

  def create_return(self, result, columns_name):
    for i in result.get("result"):
        movielist = []
        for column_name in columns_name:
          
            key = column_name.keys()[0]
            count = 1
            for data in i.get(key).items():
              if count == 1:
                movielist.append(str(data[1]))
              elif count == 2:
                movie_date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
                movielist.append(movie_date)
              elif count == 3:
                movie_date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
                movielist.append(movie_date)

              count += 1
        
        self.values.append(movielist)


class MoviesByYear(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     self.title = "Movies By Year"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    {"$group":{"_id":"$movies.Year", 
                              "count": {"$sum": 1}
                              }
                    },
                    {"$sort": SON([("_id", -1), ("count", -1)])}
                   ]
     self.columns = [{"_id" :"str"}, {"count" : "int"}]
     IMDBAggregation.__init__(self)

class MoviesByGenres(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
     self.collection = movie_collection
     self.title = "Movies By Genres"
     self.query =  [
                    { "$match": {"userid" : imdbid} },
                    { "$unwind": '$movies' },
                    {"$group":{"_id":"$movies.Genres", 
                              "count": {"$sum": 1}
                              }
                    },
                    {"$sort": SON([("count", -1)])}
                   ]
     self.columns = [{"_id" :"str"}, {"count" : "int"}]
     IMDBAggregation.__init__(self)

  def create_return(self, result, first_column_name):
    movies_genres = {}
    for movies in result.get('result'):
      for genre in movies.get("_id").split(","):
        genre_name = genre.strip()
        if  movies_genres.has_key(genre_name):
          movies_genres[genre.strip()] += 1
        else:
          movies_genres[genre.strip()] = 1

    for key, value in movies_genres.items():
      self.values.append([key.encode("utf-8"), value])



class TotalMinutesWatched(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
      self.collection = movie_collection
      self.title = "Total Time Watched"
      self.query = [
                      { "$match": {"userid" : imdbid} },
                      { "$unwind": '$movies' },
                      {"$group":{"_id":"", 
                                 "sum_runtime": {"$sum": "$movies.Runtime (mins)"}
                                 }
                      }
                   ]
      self.columns = [{"sum_runtime" : "int"}]
      IMDBAggregation.__init__(self)

  def create_return(self, result, first_column_name):
    total_hours = result.get("result")[0].get("sum_runtime") / 60
    total_days = total_hours / 24
    self.values =  str(total_hours) + " hours, or " + str(total_days) + " days."


class MovieRateByYear(IMDBAggregation):
  def __init__(self, movie_collection, imdbid):
      self.collection = movie_collection
      self.title = "Movie Rate By Year"
      self.query = [
                      { "$match": {"userid" : imdbid} },
                      { "$unwind": '$movies' },
                      {"$group":{"_id":"$movies.Year", 
                                 "avg": {"$avg": "$movies.rated"}
                                }
                      },
                      {"$sort": SON([("_id", -1), ("avg", -1)])}
                    ]
      self.columns = [{"_id" :"str"}, {"avg" :"float"}]
      IMDBAggregation.__init__(self)

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    MongoDBConnection()
