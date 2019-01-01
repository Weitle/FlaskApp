import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 获取 name 和 url 字段
sites = collection.find({}, {'_id': 0, 'name': 1, 'url': 1})
for site in sites:
    print('Name: {}, URL: {}'.format(site['name'], site['url']))