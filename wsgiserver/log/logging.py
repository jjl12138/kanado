# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/24 13:59
# @File   : log
# @Project: python高级项目

import logging
import sys

logger = logging.getLogger("server_logger")  # 创建一个自定义命令的logger，可以给其设置总的日志级别
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s', datefmt='%a, %d %b %Y %H:%M:%S') # 使用自定义日期个数

ch = logging.StreamHandler()  # 输出到控制台
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)  # 设置Handler的日志格式
logger.addHandler(ch)
