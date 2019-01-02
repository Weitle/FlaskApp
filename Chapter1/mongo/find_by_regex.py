import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 获取 name 字段中第一个字符为 'G' 的数据
sites = collection.find({'name':{'$regex': '^G'}})
for site in sites:
    print('Id: {}, Name: {}, URL: {}'.format(site['_id'], site['name'], site['url']))