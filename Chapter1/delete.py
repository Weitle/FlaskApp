import pymysql
sql = "delete from employee where age > %d" % (21,)
db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')
try:
    cursor = db.cursor()
    cursor.execute(sql)
    # 提交数据库执行
    db.commit()
except Exception as e:
    # 发生错误时回滚
    db.rollback()
    print(u'删除数据失败')
    print(e)
else:
    # 未发生错误输出成功信息
    print(u'成功删除 %d 条数据' % cursor.rowcount)
finally:
    db.close()