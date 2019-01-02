import pymongo
client = pymongo.MongoClient('mongodb://192.168.18.16:27017/')
db = client['runoob']
collection = db['sites']
# 输出修改前的所有记录
print('Before update:')
sites = collection.find()
for site in sites:
    print(site)
# 查询 name 字段中含有 'oo' 字符的记录，将第一条记录的 alexa 属性修改为 '123'
result = collection.update_many({'name': {'$regex': 'oo'}}, {'$set': {'alexa': '123'}})
print(u'成功修改 {} 条记录'.format(result.modified_count))
# 输出修改后的所有记录
print('After update:')
sites = collection.find()
for site in sites:
    print(site)