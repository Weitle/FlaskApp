import pymysql

sql = "select * from employee where income > 1000"
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
try:
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
except:
    print('Error: unable to fetch data.')
else:
    for row in results:
        # 逐条打印结果
        print("First Name: %s, Last Name: %s, Age: %s, Gender: %s, Income: %s" % (row[0], row[1], row[2], row[3], row[4]))
finally:
    db.close()
