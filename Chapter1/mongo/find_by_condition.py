import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 设置查询条件
condition = {'name': 'runoob'}
results = collection.find(condition)
for result in results:
    print('Id: {}, Name: {}, URL: {}'.format(result['_id'], result['name'], result['url']))