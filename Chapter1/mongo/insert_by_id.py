import pymongo
client = pymongo.MongoClient('mongdodb://localhost:27017')
runoob = client['runoob']
sites2 = runoob['sites']
sites = [
    { "_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
    { "_id": 2, "name": "Google", "address": "Google 搜索"},
    { "_id": 3, "name": "Facebook", "address": "脸书"},
    { "_id": 4, "name": "Taobao", "address": "淘宝"},
    { "_id": 5, "name": "Zhihu", "address": "知乎"}
]

result = sites.insert_many(sites)
print(result.inserted_id)