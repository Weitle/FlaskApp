import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
# 输出删除前的所有记录
print('Before deleted:')
sites = collection.find()
for site in sites:
    print(site)
# 删除 name 字段中含有 'b' 字符的所有记录
result = collection.delete_many({'name': {'$regex': 'b'}})
print(u'成功删除 {} 条记录'.format(result.deleted_count))
# 输出删除后的所有记录
print('After deleted:')
sites = collection.find()
for site in sites:
    print(site)