x_data = ['1','2A','2B','2M','2N','3']
for x in x_data:
    sql = """SELECT COUNT(*) FROM Diagnosis_table INNER JOIN Patient_table ON Diagnosis_table.patient_ID = Patient_table.patient_ID
        WHERE Patient_table.gender='女' AND Diagnosis_table.vwd_type='%s'""" % (x)
    print(sql)