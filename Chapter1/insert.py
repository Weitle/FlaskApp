import pymysql
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
sql = "insert into employee values('San', 'Zhang', 21, 'M', 2500)"
try:
    cursor = db.cursor()
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误回滚
    db.rollback()
else:
    # 没发生错误输出成功信息
    print(u'%d 条数据插入成功' % cursor.rowcount)
finally:
    db.close()