"""

Create the schema of the database and then interact with it
insuring the inputs are sanatised

"""
import json
import pymongo
import datetime
import string
from random import choice

#a-z A-Z 0-9 for the generation of a <4> length code (giving ~14.8 million URLs) 
CODE_ALLOWED = string.ascii_letters + string.digits

def get_database_connection_string():
    with open('hidden/hidden-json.json', 'r') as json_file:
        c = json.loads(json_file.read()) # c == connection_string -> easier to write in the f string below

    full_connection_string = f"{c['database-precursor']}{c['database-username']}:{c['database-password']}{c['database-suffix']}"
    return full_connection_string


def get_connection_client():
    connection_string = get_database_connection_string()

    client = pymongo.MongoClient(connection_string)
    return client

"""

Will insert into the SHORTURL database
Using the shorturl database and a collection called 'urls'

"""

def calc_expiry_date(days=5):
    time_now = datetime.datetime.now()
    expiry = time_now + datetime.timedelta(days=days)

    return expiry


def get_code_length():
    with open('hidden/hidden-json.json', 'r') as json_file:
        data = json.load(json_file)
    return data.get('code-length')

"""
Generates a X-char length code which is unique
X can be changed in the future

"""

def generate_code():
    LENGTH = get_code_length()

    code = ''
    
    for i in range(LENGTH):
        code += choice(CODE_ALLOWED)

    if not code_exists(code):
        return code
    return generate_code()


def code_exists(code):
    client = get_connection_client()
    db = client['shorturl']

    collection = db['urls']

    doc = collection.find({"url_code": code}, {'url_code': 1})

    for x in doc:
        if x['url_code'] == code:
            return True
    return False
    

def insert_into(full_url):
    client = get_connection_client()
    db = client['shorturl']

    collection = db['urls']

    insertion_data = {
        "expiry_date": calc_expiry_date(),
        "full_url": full_url,
        "url_code": generate_code()
    }
    collection.insert_one(insertion_data)

    return insertion_data

def get_url_from_code(code):
    client = get_connection_client()
    db = client['shorturl']

    collection = db['urls']

    doc = collection.find({"url_code": code}, {'full_url': 1})

    for x in doc:
        if len(x['full_url']) > 1:
            return x['full_url']
    return None