import pymysql
import random
import numpy as np

def generate_random_id(n)->list:
    random_numbers = []
    for i in range(n):
        rn = random.randint(100000, 999999)

        random_numbers.append(rn)
    return random_numbers


#正常的
def generate_random_number(n,min,max)  -> list:
    random_numbers = []
    for i in range(n):
        rn = random.uniform(min,max)
        random_numbers.append(np.round(rn,3))
    return random_numbers


# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "Liumenghan0922!", "sample", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("select * from t_sample")

# 使用 fetchone() 方法获取一条数据
data= cursor.fetchone()
data_list = list(cursor.fetchall())

#2n-5个
#2m-24
for i in range(24):
    #id
    e_id = 'e'+str(random.randint(100000, 999999))
    s_id = 's'+str(random.randint(100000, 999999))
    p_id = 'p'+str(random.randint(100000, 999999))
    print(e_id,s_id,p_id)
    sql_exam = """insert into exam_result(exam_ID,sample_ID,patient_ID) values ('%s','%s','%s')"""%(e_id,s_id,p_id)
    sql_diagnosis = """insert into diagnosis (patient_ID,man_result,ill_type,vwd_type) values ('%s','%s','%s','%s')"""%(p_id,'血管性血友病','出血病','2M')
    sql_patient = """insert into patients(patient_ID) values ('%s')"""%(p_id)
    cursor.execute(sql_exam)
    cursor.execute(sql_diagnosis)
    db.commit()

#
# #插入检验数据
# sql = """insert into t_sample(ID,patient_ID,type,sample_size,creation_date, modification_date,sample_status, sample_belong,box,result)
#             values('%s','%s','%s',%f,'%s','%s','%s', '%s','%s','%s')""" % (ID, patient_ID, type, sample_size, creation_date,
#                                                             modification_date, sample_status, sample_belong,box_loc,result_flag)




# 关闭数据库连接
db.close()