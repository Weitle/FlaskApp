import pymongo
client = pymongo.MongoClient('mongodb://192.168.18.16:27017/')
db = client['runoob']
collection = db['sites']
# 查询所有记录并按 'alexa' 字段降序排序
sites = collection.find().sort('alexa', -1)
for site in sites:
    print(site)