# -*- coding: utf-8 -*-
"""
项目全局配置文件
功能：定义项目的全局配置参数，包括日志级别、超时时间、文件路径等
"""

import logging
import os
import sys

# 获取项目根目录路径
DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

# 日志配置
LOG_LEVEL = logging.DEBUG        # 文件日志输出级别
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台日志输出级别

# 接口配置
API_TIMEOUT = 60  # 接口超时时间，单位：秒

# Excel文件配置
SHEET_ID = 0  # Excel文件的sheet页索引，默认读取第一个sheet页（0表示第一个）

# 测试报告配置
REPORT_TYPE = 'allure'  # 生成的测试报告类型，支持'allure'或'tm'

# 通知配置
dd_msg = False  # 是否发送钉钉消息通知

# 文件路径配置
FILE_PATH = {
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),      # 配置文件路径
    'LOG': os.path.join(DIR_BASE, 'logs'),                    # 日志文件目录
    'YAML': os.path.join(DIR_BASE),                           # YAML测试用例目录
    'TEMP': os.path.join(DIR_BASE, 'report/temp'),            # 临时报告目录
    'TMR': os.path.join(DIR_BASE, 'report/tmreport'),         # TM报告目录
    'EXTRACT': os.path.join(DIR_BASE, 'extract.yaml'),        # 数据提取文件
    'XML': os.path.join(DIR_BASE, 'data/sql'),                # SQL文件目录
    'RESULTXML': os.path.join(DIR_BASE, 'report'),            # 结果报告目录
    'EXCEL': os.path.join(DIR_BASE, 'data', '测试数据.xls')   # Excel测试数据文件
}

# 默认HTTP请求头配置
LOGIN_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}
