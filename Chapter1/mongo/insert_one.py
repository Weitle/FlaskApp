import pymongo
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
# 创建数据库
db = mongo_client['runoob']
# 创建集合
collection = db['sites']

# 由于在集合中没插入文档，此时数据库和集合都未真正创建成功
dblist = mongo_client.list_database_names()
print('已有数据库：', dblist)
collections = db.list_collection_names()
print('当前数据库中的集合列表：', collections)

# 向集合中插入文档
doc = {'name': 'runoob', 'url': 'https://www.runoob.com'}
result = collection.insert_one(doc)
print(result)

# 插入文档后，集合和数据库真正被创建
dblist = mongo_client.list_database_names()
print('已有数据库：', dblist)
collections = db.list_collection_names()
print('当前数据库中的集合列表：', collections)