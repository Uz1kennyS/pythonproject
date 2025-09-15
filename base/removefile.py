# -*- coding: utf-8 -*-
"""
文件清理工具
功能：提供文件删除和目录清理的功能，用于测试前后的数据清理
"""

import os
from common.recordlog import logs


def remove_file(filepath, endlst):
    """
    删除指定目录下指定后缀的文件
    功能：根据文件后缀批量删除文件，用于清理测试产生的临时文件
    
    Args:
        filepath (str): 要清理的文件目录路径
        endlst (list): 要删除的文件后缀列表，例如：['json','txt','attach']
        
    Returns:
        None
    """
    try:
        if os.path.exists(filepath):
            # 获取该目录下所有文件名称
            dir_lst_files = os.listdir(filepath)
            for file_name in dir_lst_files:
                fpath = filepath + '\\' + file_name
                # endswith判断字符串是否以指定后缀结尾
                if isinstance(endlst, list):
                    for ft in endlst:
                        if file_name.endswith(ft):
                            os.remove(fpath)
                else:
                    raise TypeError('file Type error,must is list')
        else:
            os.makedirs(filepath)
    except Exception as e:
        logs.error(e)


def remove_directory(path):
    """
    删除指定目录
    功能：删除指定的目录或文件
    
    Args:
        path (str): 要删除的目录或文件路径
        
    Returns:
        None
    """
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        logs.error(e)
