import pymysql

db = pymysql.connect('localhost', 'testuser', 'test123', 'testdb')

try:
    cursor = db.cursor()
    cursor.execute('drop table if exists employee')
    sql = '''create table if not exists employee(
                first_name char(20) not null,
                last_name char(20) not null,
                age smallint unsigned,
                gender char(1) default 'M',
                income float(8, 2) default 0
            ) ENGINE=InnoDB DEFAULT CHARSET utf8'''
    cursor.execute(sql)
    print('table employee is created.')
except Exception as e:
    print('Error: ', e)
finally:
    db.close()