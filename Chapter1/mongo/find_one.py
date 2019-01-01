import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 查询一条数据
doc = collection.find_one()
print(doc)
print('Id: ', doc['_id'])
print('Name: ', doc['name'])
print('URL: ', doc['url'])
