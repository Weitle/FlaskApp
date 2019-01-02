import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 返回3条记录
sites = collection.find().limit(3)
for site in sites:
    print('Id: {}, Name: {}, URL: {}'.format(site['_id'], site['name'], site['url']))