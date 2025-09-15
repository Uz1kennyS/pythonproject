# -*- coding: utf-8 -*-
"""
自动化测试框架主入口文件
功能：根据配置的测试报告类型执行测试用例并生成相应的测试报告
支持的报告类型：allure报告、tm报告
"""

import shutil
import pytest
import os
import webbrowser
from conf.setting import REPORT_TYPE

if __name__ == '__main__':
    """
    主程序入口
    根据conf/setting.py中配置的REPORT_TYPE决定生成哪种类型的测试报告
    """

    if REPORT_TYPE == 'allure':
        # 执行pytest测试并生成allure报告
        # -s: 显示print输出
        # -v: 详细输出
        # --alluredir: 指定allure报告数据目录
        # --clean-alluredir: 清理之前的报告数据
        # --junitxml: 生成junit格式的xml报告
        pytest.main(
            ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])

        # 复制环境配置文件到报告目录
        shutil.copy('./environment.xml', './report/temp')
        # 启动allure服务并自动打开浏览器
        os.system(f'allure serve ./report/temp')

    elif REPORT_TYPE == 'tm':
        # 执行pytest测试并生成tm报告
        # --pytest-tmreport-name: 指定报告文件名
        # --pytest-tmreport-path: 指定报告输出路径
        pytest.main(['-vs', '--pytest-tmreport-name=testReport.html', '--pytest-tmreport-path=./report/tmreport'])
        # 自动打开生成的测试报告
        webbrowser.open_new_tab(os.getcwd() + '/report/tmreport/testReport.html')
