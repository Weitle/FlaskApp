import pymysql

sql = "update employee set age = age + 1 where gender = 'M'"
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
try:
    cursor = db.cursor()
    cursor.execute(sql)
    # 提交数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()
    print(u'更新数据失败')
else:
    # 未发生错误输出成功信息
    print(u'成功更新 %d 条数据' % cursor.rowcount)
finally:
    db.close()