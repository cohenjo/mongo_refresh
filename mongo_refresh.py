
# Imports for the CLI using click
import click
import click_completion
import requests
import time
from yaspin import yaspin

# Imports for mongo
import pymongo
import json
from pymongo.errors import BulkWriteError
from pprint import pprint

# Imports for bing maps
import os
import io
import geocoder
from PIL import Image


################### Mongo Queries ###################

def create_state_index(db):
    result = db.zip_code.create_index('state')
    print(sorted(list(db.zip_code.index_information())))

def q1(db):
    """
    Q1) count the number of states
    """
    pipeline = [
        { "$group": { "_id": "$state"}  },
        { "$group": { "_id": 1, "count": { "$sum": 1 } } }
        ];
    res = list(db.zip_code.aggregate(pipeline))
    print("Q1: %s" % res)

def q2(db):
    """
    Q2) Print how many cities has population > 10k
    """
    results = db.zip_code.find({"pop": { "$gt": 10000 }})
    results_count = results.count()
    print("Q2: There are %d cities with population grater then 10k." % results_count)
    return results_count;

def q3(db):
    """
    Q3) We have 3 parts here:
  1) Print all the cities with population between 500 and 20000, in the states "MA" or "NH"
  2) Print the sum of the above states cities population count, per state.
  3) Print how much population there is per state except from the states above ("MA", "NH")
  """
    result = db.zip_code.find({"state": {"$in": ["MA", "NH"]}, "pop": { "$gt": 500, "$lt":20000 }},{"city":1,"_id":0})
    print("Q3-1:")
    for doc in result:
        print(doc)

    pipeline = [
        { "$match": {"state": {"$in": ["MA", "NH"]}, "pop": { "$gt": 500, "$lt":20000 }}},
        { "$group": { "_id": "$state", "count": { "$sum": "$pop" }}  }
        ];
    res = list(db.zip_code.aggregate(pipeline))
    print("Q3-2: ")
    pprint(res)
    
    pipeline = [
        { "$match": {"state": {"$nin": ["MA", "NH"]}}},
        { "$group": { "_id": "$state", "count": { "$sum": "$pop" }}  }
        ];
    res = list(db.zip_code.aggregate(pipeline))    
    print("Q3-3: ")
    pprint(res)

def q4(db):
    for result in db.zip_code.find({}, {"city": 1, "pop": 1, "_id": 0}).sort("pop", pymongo.DESCENDING).limit(1):
        print("Q4: %s" % result)
    
def q5(db):
    """
    Q5) Add to the loc array, to all documents of state: "NY", additional location element 999.
    """
    result = db.zip_code.update_many({"state": "NY"},{ "$addToSet": { "loc": 999 }})
    print("Q5: Number of Documents updated: %s" % result.modified_count)
    
def q6(db):
    """
    Q6) Remove all the cities with population less than 1k.
    """
    result = db.zip_code.remove({"pop": { "$lt": 1000 }})
    print("Q6: %s" % result)
 
########## Location Queries #############################
def q7(db):
    """
    Q7) Reverse lookup a GPS point
    """
    g = geocoder.bing([40.7943, -73.970859], method='reverse')
    pprint(g.json)


def q8(db, bingKey):
    """
    Q8) Show Location Image
    """

    URL = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road/Bellevue%20Washington?mapLayer=TrafficFlow&key="
    image_data = requests.get(URL+bingKey)
    # pprint(image_data)
    image = Image.open(io.BytesIO(image_data.content))
    image.show()

def q9(db, bingKey):
    """
    Q9) Show Distance Matrix
    """
    URL = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=47.6044,-122.3345;47.6731,-122.1185;47.6149,-122.1936&destinations=45.5347,-122.6231;47.4747,-122.2057&travelMode=driving&o=json&key="
    response = requests.get(URL+bingKey)
    pprint(response.json())


def q10(db, bingKey):
    """
    Q10) Show Route Image
    """

    URL = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?wp.0=Seattle,WA;64;1&wp.1=Redmond,WA;66;2&key="
    image_data = requests.get(URL+bingKey)
    image = Image.open(io.BytesIO(image_data.content))
    image.show()


###############################################################################
################################  CLI  ########################################
###############################################################################

@click.group()
@click.option('--user', default="admin", help='db username')
@click.option('--password', default="admin", help='db password')
@click.option('--port', default=27017, help='db port')
@click.option('--host', default="localhost", help='databases server host')
@click.pass_context
def cli(ctx, user,password,port, host):
    """
    \b
                                                                                  ______                               __       
                                                                                 /      \                             /  |      
 _____  ____    ______   _______    ______    ______          ______    ______  /$$$$$$  |______    ______    _______ $$ |____  
/     \/    \  /      \ /       \  /      \  /      \        /      \  /      \ $$ |_ $$//      \  /      \  /       |$$      \ 
$$$$$$ $$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |      /$$$$$$  |/$$$$$$  |$$   |  /$$$$$$  |/$$$$$$  |/$$$$$$$/ $$$$$$$  |
$$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |  $$/ $$    $$ |$$$$/   $$ |  $$/ $$    $$ |$$      \ $$ |  $$ |
$$ | $$ | $$ |$$ \__$$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |      $$ |      $$$$$$$$/ $$ |    $$ |      $$$$$$$$/  $$$$$$  |$$ |  $$ |
$$ | $$ | $$ |$$    $$/ $$ |  $$ |$$    $$ |$$    $$/______ $$ |      $$       |$$ |    $$ |      $$       |/     $$/ $$ |  $$ |
$$/  $$/  $$/  $$$$$$/  $$/   $$/  $$$$$$$ | $$$$$$//      |$$/        $$$$$$$/ $$/     $$/        $$$$$$$/ $$$$$$$/  $$/   $$/ 
                                  /  \__$$ |        $$$$$$/                                                                     
                                  $$    $$/                                                                                     
                                   $$$$$$/                                                                                      
                                                                                                                                
    mongo refresh - a refresho on mongo in python.
    """

    ctx.ensure_object(dict)

    shared_context = ctx.obj
    shared_context['user'] = user
    shared_context['user'] = password
    shared_context['user'] = port
    shared_context['user'] = host 
    shared_context['db_name'] = 'zip_code'
    
    BingMapsAPIKey = os.environ['BING_API_KEY']
    shared_context['BingMapsAPIKey'] = BingMapsAPIKey

    client = pymongo.MongoClient('localhost', 27017,username=user, password=password, authSource='admin')
    db = client.zip_code

    shared_context['client'] = client
    shared_context['db'] = db



@cli.command('load')
@click.pass_context
def load_data(ctx):
    db = ctx.obj['db']

    with yaspin(text="Importing...", color="yellow") as sp:

        db.zip_code.drop()
        sp.write("> Data Dropped")

        bulk = db.zip_code.initialize_ordered_bulk_op()
        sp.write("> Bulk Op Initialized")
        # Note - usually don't do this - you might crash on too much memory - read with limit to a buffer...

        response = requests.get('http://media.mongodb.org/zips.json')
        sp.write("> Data Requested")

        for line in response.iter_lines():
            if line:
                bulk.insert(json.loads(line))
        sp.write("> Bulk Ready")
        try:
            result = bulk.execute()
            sp.hide()
            pprint(result)
            sp.show()
            sp.ok("✅ ")
        except BulkWriteError as bwe:
            sp.hide()
            pprint(bwe.details)
            sp.show()
            sp.fail("💥 ")



@cli.command('queries')
@click.pass_context
def queries(ctx):
    db = ctx.obj['db']
    
    start = time.time()
    q1(db)
    q3(db)
    q5(db)
    end = time.time()
    print("it took: {}".format(end - start))

    create_state_index(db)
    start = time.time()
    q1(db)
    q3(db)
    q5(db)
    end = time.time()
    print("it took: {}".format(end - start))

    q2(db)
    q4(db)
    q6(db)

    



@cli.command('bingmaps')
@click.pass_context
def bingmaps(ctx):
    db = ctx.obj['db']
    BingMapsAPIKey = ctx.obj['BingMapsAPIKey']
    q7(db)
    q8(db,BingMapsAPIKey)
    q9(db,BingMapsAPIKey)
    q10(db,BingMapsAPIKey)

