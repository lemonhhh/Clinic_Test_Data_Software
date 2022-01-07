import datetime
from datetime import date



begin = datetime.date(2021, 11, 10)
end = date.today()
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
sql = """select * from t_sample where t_sample.creation_date like '%%%%%s%%%%' """ % today_date
print(sql)

for i in range((end - begin).days + 1):
    this_date = str(begin + datetime.timedelta(days=i))
    # this_count = 每天的
    print(this_date)
    count_sql = """SELECT COUNT(*) FROM(select date_format(creation_date, '%%Y-%%m-%%d') as dates from t_sample) tmp WHERE tmp.dates = '%s' """ % this_date

    print(count_sql)