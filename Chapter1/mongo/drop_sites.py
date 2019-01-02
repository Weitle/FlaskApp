import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 删除集合前查看集合是列表
print('Before droped:')
collections = db.list_collection_names()
print('collections', collections)
# 删除集合后查看集合列表
collection.drop()
print('After droped:')
collections = db.list_collection_names()
print('collections', collections)
