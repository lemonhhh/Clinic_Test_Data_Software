# 使用UTF-8标准编码避免中文乱码
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox, QMainWindow
import configparser
import logging
import logging.handlers
import pymysql
from pymysql import Connection

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(threadName)s - %(lineno)d - %(message)s"


# 获取erlogger
def get_logger(log_name: str, default_level=logging.DEBUG) -> tuple:
    logger = logging.getLogger(log_name)
    logger.setLevel(default_level)

    debug_handler = logging.handlers.TimedRotatingFileHandler('Log/debug.log',
                                                              when='midnight',
                                                              interval=1,
                                                              backupCount=7)

    debug_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    error_handler = logging.FileHandler('Log/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)

    return logger


# 获取ini文件处理对象
def get_ini_parser(name, encoding_pattern='utf-8'):
    """
    获取ini文件处理对象
    :param name: 配置文件名称
    :param encoding_pattern:文件编码方式
    :return:
    """
    parser = configparser.ConfigParser()  # 初始化读取对象【conf】
    parser.read(name, encoding=encoding_pattern)  # 读取配置文件
    return parser  # 返回配置文件的读取对象


# 获取sql数据库连接参数
def get_sql_paramter():
    #直接在函数里传递的
    parser = get_ini_parser("Config/SQL.ini", 'utf-8')
    item_data = parser.items("SQL")
    return {key: value for key, value in item_data}


# 获取数据库连接
def get_sql_connection() -> Connection:
    sql_dict = get_sql_paramter()
    connection = set_sql_paramter(sql_dict)

    return connection


# 设置sql数据库参数
def set_sql_paramter(sql_dict: dict) -> Connection:
    connection = pymysql.connect(host=sql_dict.get("host"),
                                 user=sql_dict.get("user"),
                                 password=sql_dict.get("password"),
                                 port=int(sql_dict.get("port")),
                                 database=sql_dict.get("database"))
    return connection


# 判断连接是否有效
def is_connection_valid(connection: Connection) -> bool:
    return True if connection is not None else False


#显示错误信息
def show_error_message(self, message: str) -> None:
    QMessageBox.warning(self, "温馨提示", message, QMessageBox.Ok)


# 显示正确信息
def show_successful_message(self, message: str) -> None:
    QMessageBox.information(self, "温馨提示", message, QMessageBox.Ok)