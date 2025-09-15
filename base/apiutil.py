# -*- coding: utf-8 -*-
"""
API接口测试基础工具类
功能：提供接口测试的核心功能，包括参数替换、接口请求、数据提取、断言等
"""

import json
import re
from json.decoder import JSONDecodeError

import allure
import jsonpath

from common.assertions import Assertions
from common.debugtalk import DebugTalk
from common.readyaml import get_testcase_yaml, ReadYamlData
from common.recordlog import logs
from common.sendrequest import SendRequest
from conf.operationConfig import OperationConfig
from conf.setting import FILE_PATH


class RequestBase:
    """
    接口测试基础类
    功能：
    1. 解析YAML测试用例文件
    2. 处理参数替换和动态数据生成
    3. 发送HTTP请求
    4. 提取响应数据
    5. 执行断言验证
    """

    def __init__(self):
        """
        初始化RequestBase类
        创建各个功能模块的实例对象
        """
        self.run = SendRequest()  # HTTP请求发送器
        self.conf = OperationConfig()  # 配置文件读取器
        self.read = ReadYamlData()  # YAML文件读写器
        self.asserts = Assertions()  # 断言验证器

    def replace_load(self, data):
        """
        YAML数据动态替换解析
        功能：将YAML文件中的${函数名(参数)}格式的字符串替换为实际值
        
        Args:
            data: 需要替换的数据，可以是字符串、字典或列表
            
        Returns:
            替换后的数据
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
            # print('从yaml文件获取的原始数据：', str_data)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出yaml文件的函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # 取出函数里面的参数
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值,类的反射----getattr,setattr,del....
                extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")

                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_params, str(extract_data))
                # print('通过解析后替换的数据：', str_data)

        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, base_info, test_case):
        """
        接口请求处理核心方法
        功能：解析YAML测试用例，发送HTTP请求，处理响应数据，执行断言
        
        Args:
            base_info (dict): YAML文件中的baseInfo部分，包含接口基本信息
            test_case (dict): YAML文件中的testCase部分，包含测试用例数据
            
        Returns:
            None
        """
        try:
            params_type = ['data', 'json', 'params']
            url_host = self.conf.get_section_for_data('api_envi', 'host')
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            url = url_host + base_info['url']
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            header = self.replace_load(base_info['header'])
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # 处理cookie
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # 处理断言
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))
            # 处理参数提取
            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)
            # 处理接口的请求参数
            for key, value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)

            # 处理文件上传接口
            file, files = test_case.pop('files', None), None
            if file is not None:
                for fk, fv in file.items():
                    allure.attach(json.dumps(file), '导入文件')
                    files = {fk: open(fv, mode='rb')}

            res = self.run.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                    file=files, cookies=cookie, **test_case)
            status_code = res.status_code
            allure.attach(self.allure_attach_response(res.json()), '接口响应信息', allure.attachment_type.TEXT)

            try:
                res_json = json.loads(res.text)  # 把json格式转换成字典字典
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, status_code)
            except JSONDecodeError as js:
                logs.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                logs.error(e)
                raise e

        except Exception as e:
            raise e

    @classmethod
    def allure_attach_response(cls, response):
        """
        格式化响应数据用于Allure报告展示
        
        Args:
            response: 接口响应数据
            
        Returns:
            str: 格式化后的响应数据字符串
        """
        if isinstance(response, dict):
            allure_response = json.dumps(response, ensure_ascii=False, indent=4)
        else:
            allure_response = response
        return allure_response

    def extract_data(self, testcase_extarct, response):
        """
        提取接口返回值（单个参数）
        功能：支持正则表达式和JSON路径两种方式提取响应数据
        
        Args:
            testcase_extarct (dict): YAML文件中定义的extract提取规则
            response (str): 接口的实际响应文本
            
        Returns:
            None: 提取的数据会写入extract.yaml文件
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml_data(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml_data(extarct_data)
        except Exception as e:
            logs.error(e)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数（列表形式）
        功能：支持正则表达式和JSON路径提取，结果以列表形式返回
        
        Args:
            testcase_extract_list (dict): YAML文件中定义的extract_list提取规则
            response (str): 接口的实际响应文本
            
        Returns:
            None: 提取的数据会写入extract.yaml文件
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    case_info = get_testcase_yaml(FILE_PATH['YAML'] + '/LoginAPI/login.yaml')[0]
    # print(case_info)
    req = RequestBase()
    # res = req.specification_yaml(case_info)
    res = req.specification_yaml(case_info)
    print(res)
