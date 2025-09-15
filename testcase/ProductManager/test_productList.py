# -*- coding: utf-8 -*-
"""
商品管理模块测试用例
功能：测试商品管理相关的接口，包括商品列表、商品详情、订单提交、订单支付等
"""

import allure
import pytest

from base.generateId import m_id, c_id
from base.apiutil import RequestBase
from common.readyaml import get_testcase_yaml


@allure.feature(next(m_id) + '商品管理（单接口）')
class TestLogin:
    """
    商品管理测试类
    功能：测试商品管理模块的各个接口功能
    """

    @allure.story(next(c_id) + "获取商品列表")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/getProductList.yaml'))
    def test_get_product_list(self, base_info, testcase):
        """
        测试获取商品列表接口
        功能：验证商品列表接口的返回数据格式和内容
        """
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "获取商品详情信息")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/productDetail.yaml'))
    def test_get_product_detail(self, base_info, testcase):
        """
        测试获取商品详情接口
        功能：验证商品详情接口的返回数据格式和内容
        """
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    # @allure.story('检查接口状态')
    # @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/productManager/apiType.yaml'))
    # def test_get_api_type(self, params):
    #     RequestBase().specification_yaml(params)
    #
    # @allure.story('电网系统登录校验')
    # @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/productManager/login_dw.yaml'))
    # def test_get_login_dw(self, params):
    #     RequestBase().specification_yaml(params)

    @allure.story(next(c_id) + "提交订单")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/commitOrder.yaml'))
    def test_commit_order(self, base_info, testcase):
        """
        测试提交订单接口
        功能：验证订单提交接口的业务逻辑和返回结果
        """
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "订单支付")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml('./testcase/ProductManager/orderPay.yaml'))
    def test_order_pay(self, base_info, testcase):
        """
        测试订单支付接口
        功能：验证订单支付接口的业务逻辑和返回结果
        """
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)
