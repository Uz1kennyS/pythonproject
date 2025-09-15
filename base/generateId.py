# -*- coding: utf-8 -*-
"""
测试用例ID生成器
功能：为测试模块和测试用例生成唯一编号，确保Allure报告的顺序与pytest执行顺序一致
"""


def generate_module_id():
    """
    生成测试模块编号
    功能：为测试模块生成M01_、M02_等格式的编号
    目的：保证Allure报告的顺序与pytest设定的执行顺序保持一致
    
    Yields:
        str: 格式为M01_、M02_...M999_的模块编号
    """
    for i in range(1, 1000):
        module_id = 'M' + str(i).zfill(2) + '_'  # 使用zfill确保编号为两位数
        yield module_id


def generate_testcase_id():
    """
    生成测试用例编号
    功能：为测试用例生成C01_、C02_等格式的编号
    
    Yields:
        str: 格式为C01_、C02_...C9999_的用例编号
    """
    for i in range(1, 10000):
        case_id = 'C' + str(i).zfill(2) + '_'  # 使用zfill确保编号为两位数
        yield case_id


# 创建生成器实例，供其他模块使用
m_id = generate_module_id()  # 模块ID生成器
c_id = generate_testcase_id()  # 用例ID生成器
