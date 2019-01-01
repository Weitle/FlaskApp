import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['runoob']

# 创建集合 sites
sites = mydb['sites']
print(sites)