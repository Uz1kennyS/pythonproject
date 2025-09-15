# -*- coding: utf-8 -*-
"""
HTTP请求发送器
功能：封装HTTP请求发送功能，支持GET、POST等方法，提供请求日志记录和响应处理
"""

import json
import allure
import pytest
import requests
import urllib3
import time

from conf import setting
from common.recordlog import logs
from requests import utils
from common.readyaml import ReadYamlData
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class SendRequest:
    """
    HTTP请求发送器类
    功能：
    1. 发送GET、POST等HTTP请求
    2. 处理请求参数和响应数据
    3. 记录请求日志
    4. 支持文件上传
    5. 自动处理Cookie
    """

    def __init__(self, cookie=None):
        """
        初始化SendRequest类
        
        Args:
            cookie (dict, optional): 初始Cookie信息
        """
        self.cookie = cookie
        self.read = ReadYamlData()

    def get(self, url, data, header):
        """
        发送GET请求
        功能：发送HTTP GET请求并返回响应数据
        
        Args:
            url (str): 接口地址
            data (dict): 请求参数
            header (dict): 请求头
            
        Returns:
            dict: 包含响应状态码、响应文本、响应时间等信息的字典
        """
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.get(url, headers=header, cookies=self.cookie, verify=False)
            else:
                response = requests.get(url, data, headers=header, cookies=self.cookie, verify=False)
        except requests.RequestException as e:
            logs.error(e)
            return None
        except Exception as e:
            logs.error(e)
            return None
        # 响应时间/毫秒
        res_ms = response.elapsed.microseconds / 1000
        # 响应时间/秒
        res_second = response.elapsed.total_seconds()
        response_dict = dict()

        # 接口响应状态码
        response_dict['code'] = response.status_code
        # 接口响应文本
        response_dict['text'] = response.text
        try:
            response_dict['body'] = response.json().get('body')
        except Exception:
            response_dict['body'] = ''
        response_dict['res_ms'] = res_ms
        response_dict['res_second'] = res_second
        return response_dict

    def post(self, url, data, header):
        """
        发送POST请求
        功能：发送HTTP POST请求并返回响应数据
        
        Args:
            url (str): 接口地址
            data (dict): 请求参数，verify=False忽略SSL证书验证
            header (dict): 请求头
            
        Returns:
            dict: 包含响应状态码、响应文本、响应时间等信息的字典
        """
        # 控制台输出InsecureRequestWarning错误
        requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if data is None:
                response = requests.post(url, header, cookies=self.cookie, verify=False)
            else:
                response = requests.post(url, data, headers=header, cookies=self.cookie, verify=False)
        except requests.RequestException as e:
            logs.error(e)
            return None
        except Exception as e:
            logs.error(e)
            return None
        # 响应时间/毫秒
        res_ms = response.elapsed.microseconds / 1000
        # 响应时间/秒
        res_second = response.elapsed.total_seconds()
        response_dict = dict()
        # 接口响应状态码
        response_dict['code'] = response.status_code
        # 接口响应文本
        response_dict['text'] = response.text
        try:
            response_dict['body'] = response.json().get('body')
        except Exception:
            response_dict['body'] = ''
        response_dict['res_ms'] = res_ms
        response_dict['res_second'] = res_second
        return response_dict

    def send_request(self, **kwargs):
        """
        发送HTTP请求的通用方法
        功能：使用requests.session发送请求，自动处理Cookie和异常
        
        Args:
            **kwargs: requests.request()方法的所有参数
            
        Returns:
            requests.Response: HTTP响应对象
        """
        session = requests.session()
        result = None
        cookie = {}
        try:
            result = session.request(**kwargs)
            # 提取响应中的Cookie并保存
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml_data(cookie)
                logs.info("cookie：%s" % cookie)
            logs.info("接口返回信息：%s" % result.text if result.text else result)
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        """
        接口请求主方法
        功能：发送HTTP请求并记录详细的请求日志，支持Allure报告集成
        
        Args:
            name (str): 接口名称
            url (str): 接口地址
            case_name (str): 测试用例名称
            header (dict): 请求头
            method (str): 请求方法（GET、POST等）
            cookies (dict, optional): Cookie信息，默认为空
            file (dict, optional): 文件上传参数
            **kwargs: 其他请求参数，根据YAML文件的参数类型
            
        Returns:
            requests.Response: HTTP响应对象
        """

        try:
            # 收集报告日志
            logs.info('接口名称：%s' % name)
            logs.info('请求地址：%s' % url)
            logs.info('请求方式：%s' % method)
            logs.info('测试用例名称：%s' % case_name)
            logs.info('请求头：%s' % header)
            logs.info('Cookie：%s' % cookies)
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if "data" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        # time.sleep(0.5)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = self.send_request(method=method,
                                     url=url,
                                     headers=header,
                                     cookies=cookies,
                                     files=file,
                                     timeout=setting.API_TIMEOUT,
                                     verify=False,
                                     **kwargs)
        return response
