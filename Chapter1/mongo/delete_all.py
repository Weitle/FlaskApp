import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 输出删除前的所有记录
print('Before deleted:')
sites = collection.find()
for site in sites:
    print(site)

# 删除所有记录
result = collection.delete_many({})
print(u'成功删除 {} 条记录'.format(result.deleted_count))
# 输出删除后的所有记录
print('After deleted:')
sites = collection.find()
print('Count of sites:', sites.count())

# 查看集合是否还存在
collections = db.list_collection_names()
if 'sites' in collections:
    print('集合还存在')
else:
    print('集合已不存在')