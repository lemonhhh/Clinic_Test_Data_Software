from Util.Common import get_sql_connection, get_logger, show_error_message, show_successful_message
import random


def set_connection_cursor():
    connection = None
    cursor = None
    connection = get_sql_connection()
    cursor = connection.cursor()
    return connection,cursor

def set_logger():
    logger = get_logger("my_logger")
    return logger

def get_sql(self):

    sql = """select * from patients"""
    return sql

if __name__ == '__main__':
    connection,cursor = set_connection_cursor()
    sql= get_sql()
    # cursor.execute(sql)
    # connection.commit()
