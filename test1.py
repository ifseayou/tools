#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/08 17:48:55
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

import schedule
import time

# 定义你要周期运行的函数
def job():
    print("I'm working...")

if __name__ == '__main__':

    # schedule.every().second.do(job)                    # 每隔 1 小时运行一次 job 函数
    
    # schedule.every().friday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
    schedule.every().monday.at("18:24").do(job)   # 每周三 13：15 时间点运行 job 函数

    while True:
        schedule.run_pending()   # 运行所有可以运行的任务
        time.sleep(1)
        
