import pymysql
import random
import numpy as np




# 打开数据库连接
#db = pymysql.connect("127.0.0.1", "root", "Liumenghan0922!", "sample", charset='utf8')

mydb = pymysql.connect(
    host="81.69.170.44",  # 数据库主机地址
    port=3306,
    user="root",  # 数据库用户名
    password="Asdf0506",  # 数据库密码
    database="Sample",
    charset='utf8'
)

# 使用cursor()方法获取操作游标
cursor = mydb.cursor()

sql = """select * from Diagnosis_table limit 1"""
cursor.execute(sql)
print(cursor.fetchall())

mydb.close()