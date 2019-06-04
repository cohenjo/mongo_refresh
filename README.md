
# mongo_refresh

There comes a time in a programmers life that he must refresh on mongo using python.
My time has come - so I'm refreshing :)

*Note:* This is an overkill to what this actually does - but it removes a bit of rust off my python.
*2nd Note:* Really nothing interesting to see... just rambling on GitHub...


![](docs/example.gif)
## Features
* loads zip data off [zip code sample data](http://media.mongodb.org/zips.json)
* perform queries
* perform aggregations
* Play with Bing Maps API



## Installation
* clone mongo_refresh
```shell
git clone git@github.com:cohenjo/mongo_refresh.git

cd mongo_refresh
```

* set vritual environment
```shell
pip install virtualenv
virtualenv -p /usr/local/bin/python3.7 venv
. ./venv/bin/activate
```

* install mongo_refresh
```shell
pip install -e .
```

* run mongo_refresh help
```shell
mongo_refresh --help
```

## Usage

### Loading Data
For Start we'll upload the following json data file, to collection zip_code, using python program, to mongo: 
http://media.mongodb.org/zips.json

```bash
mongo_refresh --user mongoadmin --password secret load
```

### Sample Queries, aggregations, DML etc...
Let's answers the following questions: 
Q1) Print how many distinct states in this file ?
Q2) Print how many cities has population > 10000
Q3) We have 3 parts here:
  1) Print all the cities with population between 500 and 20000, in the states "MA" or "NH"
  2) Print the sum of the above states cities population count, per state.
  3) Print how much population there is per state except from the states above ("MA", "NH")
Q4) Print the city with the max population, with its population number.
Q5) Add to the loc array, to all documents of state: "NY", additional location element 999.
Q6) Remove all the cities with population less than 1k.

```bash
mongo_refresh --user mongoadmin --password secret queries
```

Maybe I'll add example on how to index the zip_code collection, in order to support best the queries above. 
I'll explain what changes done and why. (pre/post with timing, maybe?)


### Bing Maps
play with bing maps
Q7) Reverse lookup a GPS point
Q8) Show Location Image
Q9) Show Distance Matrix
Q10) Show Route Image

```bash
export BING_API_KEY=<top secret bing API Key>
mongo_refresh --user mongoadmin --password secret bingmaps
```

*Note:* For this excersize examples I used a simple local Docker:
```bash
docker run -d --name some-mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret mongo
```


## Built while playing With
* [Click](https://click.palletsprojects.com/en/7.x/) - The command line framework
* [click_completion](https://github.com/click-contrib/click-completion) - Enhanced completion for Click
* [ruamel.yaml](https://bitbucket.org/ruamel/yaml) - YAML 1.2 loader/dumper package for Python.
* [yaspin](https://github.com/pavdmyt/yaspin) - A lightweight terminal spinner for Python
* [PyInquirer](https://github.com/CITGuru/PyInquirer) - A Python module for common interactive command line user interfaces
* [deepmerge](https://pypi.org/project/deepmerge/) - A tools to handle merging of nested data structures in python.
* [Pygments](http://pygments.org/) - For terminal syntax highlighting.
* [tabulate](https://bitbucket.org/astanin/python-tabulate) - Pretty-print tabular data in Python, a library and a command-line utility.
* [pydash](https://github.com/dgilland/pydash) - The kitchen sink of Python utility libraries for doing "stuff" in a functional way
* [PyMongo](https://api.mongodb.com/python/current/) - The MongoDB Python official driver
* [geocoder](https://geocoder.readthedocs.io/providers/Bing.html) - simple and consistent geocoding library 
* [Pillow](https://python-pillow.org) - The friendly PIL fork.
