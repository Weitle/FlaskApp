import pymysql

# 打开数据库连接
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
# 使用 cursor() 方法创建一个游标对象 
cursor = db.cursor()
# 使用 execute() 方法执行查询
cursor.execute('select version()')
# 使用 fetchone() 方法获取数据
data = cursor.fetchone()
# 输出结果
print('Database version is: %s.' % data)
# 关闭数据库连接
db.close()