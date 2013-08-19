from pymongo import Connection, MongoClient

class MongoDBConnection():
    def __init__(self):
        client = MongoClient('localhost', 27021)


def main():
    print "ok"
    MongoDBConnection()

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    main()