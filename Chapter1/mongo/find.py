import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 获取所有数据
sites = collection.find()
for site in sites:
    print('Id: {}, Name: {}, URL: {}'.format(site['_id'], site['name'], site['url']))