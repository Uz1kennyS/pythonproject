def generate_test_summary(terminalreporter):
    """生成测试结果摘要字符串，兼容 pytest 7.x / 8.x"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    # 兼容 _session_start / _sessionstarttime
    start_time = getattr(terminalreporter, "_session_start", None) or getattr(terminalreporter, "_sessionstarttime", None)

    # 如果是 Instant 类型，获取 float 秒数
    if start_time is not None:
        try:
            # pytest8.x Instant 类型
            duration = time.time() - start_time.timestamp()
        except AttributeError:
            # pytest7.x 旧版 float 类型
            duration = time.time() - start_time
    else:
        duration = 0

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
