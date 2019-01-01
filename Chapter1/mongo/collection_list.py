import pymongo
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
db = myclient['runoob']
# 获取数据库对象下的所有集合列表
collections = db.list_collection_names()
if 'sites' in collections:
    print(u'集合已存在')
else:
    print(u'集合不存在')