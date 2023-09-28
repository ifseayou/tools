#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/28 10:38:36
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

import configparser

# 创建一个ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read('conf/db.ini')

# 获取特定键的值
value = config.get('impala_conf', 'impala_host')

# 打印值
print(value)
