import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
runoob = client['runoob']
sites2 = runoob['sites2']
sites = [
    { "_id": 11, "name": "RUNOOB", "cn_name": "菜鸟教程"},
    { "_id": 12, "name": "Google", "address": "Google 搜索"},
    { "_id": 13, "name": "Facebook", "address": "脸书"},
    { "_id": 14, "name": "Taobao", "address": "淘宝"},
    { "_id": 15, "name": "Zhihu", "address": "知乎"}
]

result = sites2.insert_many(sites)
print(result.inserted_ids)
