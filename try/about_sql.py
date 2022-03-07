import pymysql
import random
import numpy as np




# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "Liumenghan0922!", "sample", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

db_name = ["APTT","Ag","Act","RIPA","FV3C","CB","pp","BS"]

for item in db_name:
    sql = """select '%s' from Exam_table where '%s' is not null """%(item,item)
    print(sql)
    cursor.execute(sql)
    data_list = list(cursor.fetchall())
    print(data_list)


# 使用execute方法执行SQL语句
cursor.execute("select * from t_sample")

# 使用 fetchone() 方法获取一条数据
data= cursor.fetchone()
data_list = list(cursor.fetchall())



# 关闭数据库连接
db.close()