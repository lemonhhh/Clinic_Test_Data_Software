import pymysql

# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "Liumenghan0922!", "sample", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("select * from t_sample")

# 使用 fetchone() 方法获取一条数据
data= cursor.fetchone()
data_list = list(cursor.fetchall())




# 关闭数据库连接
db.close()
target = 18
sql = """select * from patients where age < %i """ % target
print(sql)