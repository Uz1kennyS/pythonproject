# -*- coding: utf-8 -*-
"""
配置文件操作工具类
功能：封装读取和操作*.ini配置文件的功能
"""

import sys
import traceback
import configparser
from conf import setting
from common.recordlog import logs


class OperationConfig:
    """
    配置文件操作类
    功能：封装读取和操作*.ini配置文件的功能，提供各种配置项的读取方法
    """

    def __init__(self, filepath=None):
        """
        初始化OperationConfig类
        
        Args:
            filepath (str, optional): 配置文件路径，默认使用setting中配置的路径
        """
        if filepath is None:
            self.__filepath = setting.FILE_PATH['CONFIG']
        else:
            self.__filepath = filepath

        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__filepath, encoding='utf-8')
        except Exception as e:
            exc_type, exc_value, exc_obj = sys.exc_info()
            logs.error(str(traceback.print_exc(exc_obj)))

        self.type = self.get_report_type('type')

    def get_item_value(self, section_name):
        """
        获取指定section的所有配置项
        功能：根据ini文件的section名称获取该section下的所有配置项
        
        Args:
            section_name (str): ini文件的section名称
            
        Returns:
            dict: 以字典形式返回的配置项
        """
        items = self.conf.items(section_name)
        return dict(items)

    def get_section_for_data(self, section, option):
        """
        获取指定配置项的值
        功能：根据section和option获取具体的配置值
        
        Args:
            section (str): ini文件的section名称
            option (str): section下的配置项名称
            
        Returns:
            str: 配置项的值
        """
        try:
            values = self.conf.get(section, option)
            return values
        except Exception as e:
            logs.error(str(traceback.format_exc()))
            return ''

    def write_config_data(self, section, option_key, option_value):
        """
        写入数据到ini配置文件
        功能：向ini配置文件中写入新的配置项
        
        Args:
            section (str): section名称
            option_key (str): 配置项键名
            option_value (str): 配置项值
            
        Returns:
            None
        """
        if section not in self.conf.sections():
            # 添加一个section值
            self.conf.add_section(section)
            self.conf.set(section, option_key, option_value)
        else:
            logs.info('"%s"值已存在，写入失败' % section)
        with open(self.__filepath, 'w', encoding='utf-8') as f:
            self.conf.write(f)

    def get_section_mysql(self, option):
        """
        获取MySQL配置项
        功能：从MYSQL section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data("MYSQL", option)

    def get_section_redis(self, option):
        """
        获取Redis配置项
        功能：从REDIS section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data("REDIS", option)

    def get_section_clickhouse(self, option):
        """
        获取ClickHouse配置项
        功能：从CLICKHOUSE section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data("CLICKHOUSE", option)

    def get_section_mongodb(self, option):
        """
        获取MongoDB配置项
        功能：从MongoDB section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data("MongoDB", option)

    def get_report_type(self, option):
        """
        获取报告类型配置项
        功能：从REPORT_TYPE section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data('REPORT_TYPE', option)

    def get_section_ssh(self, option):
        """
        获取SSH配置项
        功能：从SSH section中获取指定配置项
        
        Args:
            option (str): 配置项名称
            
        Returns:
            str: 配置项值
        """
        return self.get_section_for_data("SSH", option)