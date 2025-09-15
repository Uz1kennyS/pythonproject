# -*- coding: utf-8 -*-
"""
YAML文件读写工具
功能：提供YAML测试用例文件的读取、写入和解析功能
"""

import yaml
import traceback
import os

from common.recordlog import logs
from conf.operationConfig import OperationConfig
from conf.setting import FILE_PATH
from yaml.scanner import ScannerError


def get_testcase_yaml(file):
    """
    读取YAML测试用例文件
    功能：解析YAML格式的测试用例文件，返回结构化的测试数据
    
    Args:
        file (str): YAML文件路径
        
    Returns:
        list: 解析后的测试用例列表
    """
    testcase_list = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if len(data) <= 1:
                yam_data = data[0]
                base_info = yam_data.get('baseInfo')
                for ts in yam_data.get('testCase'):
                    param = [base_info, ts]
                    testcase_list.append(param)
                return testcase_list
            else:
                return data
    except UnicodeDecodeError:
        logs.error(f"[{file}]文件编码格式错误，--尝试使用utf-8编码解码YAML文件时发生了错误，请确保你的yaml文件是UTF-8格式！")
    except FileNotFoundError:
        logs.error(f'[{file}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f'获取【{file}】文件数据时出现未知错误: {str(e)}')


class ReadYamlData:
    """
    YAML数据读写类
    功能：提供YAML文件的读取、写入和数据提取功能
    """

    def __init__(self, yaml_file=None):
        """
        初始化ReadYamlData类
        
        Args:
            yaml_file (str, optional): YAML文件路径
        """
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            pass
        self.conf = OperationConfig()
        self.yaml_data = None

    @property
    def get_yaml_data(self):
        """
        获取测试用例YAML数据
        功能：读取并解析YAML文件内容
        
        Returns:
            list: 解析后的YAML数据列表
        """
        # Loader=yaml.FullLoader表示加载完整的YAML语言，避免任意代码执行，无此参数控制台报Warning
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f)
                return self.yaml_data
        except Exception:
            logs.error(str(traceback.format_exc()))

    def write_yaml_data(self, value):
        """
        写入YAML文件数据
        功能：将数据写入extract.yaml文件，主要用于接口关联和数据提取
        
        Args:
            value (dict): 要写入的数据，必须为字典格式
            
        Returns:
            None
        """

        file = None
        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            os.system(file_path)
        try:
            file = open(file_path, 'a', encoding='utf-8')  ##写入
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
            else:
                logs.info('写入[extract.yaml]的数据必须为dict格式')
        except Exception:
            logs.error(str(traceback.format_exc()))
        finally:
            file.close()

    def clear_yaml_data(self):
        """
        清空extract.yaml文件数据
        功能：清空extract.yaml文件中的所有内容
        
        Returns:
            None
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()

    def get_extract_yaml(self, node_name, second_node_name=None):
        """
        读取接口提取的变量值
        功能：从extract.yaml文件中读取指定节点的数据
        
        Args:
            node_name (str): 要读取的节点名称
            second_node_name (str, optional): 二级节点名称
            
        Returns:
            提取的数据值
        """
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            logs.error('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            logs.info('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            logs.error(f"【extract.yaml】没有找到：{node_name},--%s" % e)

    def get_testCase_baseInfo(self, case_info):
        """
        获取testcase yaml文件的baseInfo数据
        :param case_info: yaml数据，dict类型
        :return:
        """
        pass

    def get_method(self):
        """
        :param self:
        :return:
        """
        yal_data = self.get_yaml_data()
        metd = yal_data[0].get('method')
        return metd

    def get_request_parame(self):
        """
        获取yaml测试数据中的请求参数
        :return:
        """
        data_list = []
        yaml_data = self.get_yaml_data()
        del yaml_data[0]
        for da in yaml_data:
            data_list.append(da)
        return data_list
