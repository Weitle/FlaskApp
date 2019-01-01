import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['runoob']
collection = db['sites']
doc = collection.insert_one({'name': 'Google', 'url': 'https://www.google.com'})
print(doc.inserted_id)