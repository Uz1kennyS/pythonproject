# -*- coding: utf-8 -*-
"""
pytest全局配置文件
功能：定义测试结果摘要生成函数，兼容不同版本的pytest
"""

import time
import pytest

from common.readyaml import ReadYamlData


def generate_test_summary(terminalreporter):
    """
    生成测试结果摘要字符串，兼容 pytest 7.x / 8.x
    
    Args:
        terminalreporter: pytest终端报告器对象
        
    Returns:
        str: 格式化的测试结果摘要字符串
    """
    # 获取测试统计信息
    total = terminalreporter._numcollected  # 总测试用例数
    passed = len(terminalreporter.stats.get('passed', []))  # 通过数量
    failed = len(terminalreporter.stats.get('failed', []))  # 失败数量
    error = len(terminalreporter.stats.get('error', []))  # 错误数量
    skipped = len(terminalreporter.stats.get('skipped', []))  # 跳过数量

    # 兼容不同pytest版本的会话开始时间属性
    # _session_start: pytest 8.x版本
    # _sessionstarttime: pytest 7.x版本
    start_time = getattr(terminalreporter, "_session_start", None) or getattr(terminalreporter, "_sessionstarttime",
                                                                              None)

    # 计算测试执行总时长
    if start_time is not None:
        try:
            # pytest 8.x版本：Instant类型，需要调用timestamp()方法
            duration = time.time() - start_time.timestamp()
        except AttributeError:
            # pytest 7.x版本：直接是float类型
            duration = time.time() - start_time
    else:
        duration = 0

    # 生成测试结果摘要
    summary = f"""
自动化测试结果，通知如下，请着重关注测试失败的接口，具体执行结果如下：
测试用例总数：{total}
测试通过数：{passed}
测试失败数：{failed}
错误数量：{error}
跳过执行数量：{skipped}
执行总时长：{duration:.2f} 秒
"""
    print(summary)
    return summary


@pytest.fixture(scope="session", autouse=True)
def clear_data():
    ReadYamlData.clear_yaml_data(self=None)
