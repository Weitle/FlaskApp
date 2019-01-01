import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
runoob = client['runoob']
sites = runoob['sites']
mylist = [
    { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" },
    { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" },
    { "name": "Facebook", "alexa": "10", "url": "https://www.facebook.com" },
    { "name": "知乎", "alexa": "103", "url": "https://www.zhihu.com" },
    { "name": "Github", "alexa": "109", "url": "https://www.github.com" }
]

result = sites.insert_many(mylist)
# insert_many() 方法返回一个 InsertManyResult 对象
print(result)
# InsertManyResult 对象包含 inserted_ids 属性，该属性保存着所有插入文档的 id
print(result.inserted_ids)