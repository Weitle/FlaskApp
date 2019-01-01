import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = myclient.list_database_names()
if 'runoob' in dblist:
    print('数据库创建成功')
else:
    print('数据库未创建成功')