# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/24 16:43
# @File   : render_template
# @Project: python高级项目

import os
from jinja2 import Environment, FileSystemLoader

def render_template(template_name_or_list, **context):
    # 得到放置模板的目录

    path = '{}/templates/'.format(os.getcwd())  # 返回当前工作目录

    # 创建一个加载器，jinja2会从这个目录中加载模板
    loader = FileSystemLoader(path)

    # 用加载器创建一个环境，有了它才能读取模板文件
    env = Environment(loader=loader)

    # 调用get_tempalte()方法加载模板并返回
    template = env.get_template(template_name_or_list)

    html = template.render(**context)
    return html
