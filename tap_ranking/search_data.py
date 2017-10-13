from pymongo import MongoClient
import json
import re

def add_index(result):
    lists = []
    if len(result) > 0:
        keys = result[0].keys()
        for i in range(0, len(result), 1):
            dataobj = {}
            for j in keys:
                if j != "_id":
                    dataobj[j] = result[i][j]
                    dataobj["index"] = (i+1)
            lists.append(dataobj)
    return lists

# def get_rank():
#     client = MongoClient('127.0.0.1', 27017)
#     db = client.local
#     result = list(db.taplistrank20170910.find({}).sort([("install_reduce", -1)]).limit(100))
#     return result
#
# def get_rank_top():
#     client = MongoClient('127.0.0.1', 27017)
#     db = client.local
#     result = list(db.taplistrank20170911.find({}).sort([("install_reduce", -1)]).limit(100))
#     return add_index(result)

def get_Installs(time, search):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "taplistrank" + str(db_name)
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).sort([("install_reduce", -1)]).limit(100))
    return add_index(result)

def get_reserved(time, search):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "taplistrank" + str(db_name)
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).sort([("reserved_reduce", -1)]).limit(100))
    return add_index(result)

def get_attention(time, search):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "taplistrank" + str(db_name)
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).sort([("attention_reduce", -1)]).limit(100))
    return add_index(result)

def tap_ad_lists(time):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "taptapGameIndexAd" + str(db_name)
    result = list(db[db_name].find({"type": "ad"}).sort([("show_times", -1)]))
    return add_index(result)

def tap_top_game(time):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "taptapGameIndexAd" + str(db_name)
    result = list(db[db_name].find({"type": "top"}).sort([("time", -1)]))
    return add_index(result)

def tap_add_everyday(time, search):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    db_name = time.replace("-", "")
    db_name = "tap_game_id_new_add" + str(db_name)
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).sort([("game_id", -1)]))
    return add_index(result)


def check_name_pass(username, password):
    client = MongoClient('127.0.0.1', 27017)
    db = client.local
    result = list(db.userName.find({"en_name": username}))
    if (len(result) > 0) and result[0]["password"] == password:
        return True
    else:
        return False
