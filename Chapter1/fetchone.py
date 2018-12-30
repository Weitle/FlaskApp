import pymysql
sql = "select * from employee where income > 1000"
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
try:
    cursor = db.cursor()
    cursor.execute(sql)
    rowcount = cursor.rowcount
    row = cursor.fetchone()
except:
    print('Error: unable to fetch data.')
else:
    print('共 %d 条数据' % rowcount)
    print('第一条数据：')
    print("First Name: %s, Last Name: %s, Age: %s, Gender: %s, Income: %s" % (row[0], row[1], row[2], row[3], row[4]))
finally:
    db.close()