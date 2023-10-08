#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/07 17:49:25
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''


from crontab import CronTab

# 创建linux系统当前用户的crontab，当然也可以创建其他用户的，但得有足够权限,如:user='root'
cron_manager  = CronTab(user=True)

# 创建任务 指明运行python脚本的命令(crontab的默认执行路径为：当前用户的根路径, 因此需要指定绝对路径)
job = cron_manager.new(command='python /Users/xhl/work/tools/test1.py >> /Users/xhl/work/tools/logs.log 2>&1 &')

# 设置任务执行周期，每两分钟执行一次(更多方式请稍后参见参考链接)
job.setall('*/1 * * * *')

# 将crontab写入linux系统配置文件
# my_user_cron.write()

# from crontab import CronTab


# cron = CronTab(user=True)

# job = cron.new(command='echo hello world')

# # # 创建linux系统当前用户的crontab，当然也可以创建其他用户的，但得有足够权限,如:user='root'
# # cron_manager  = CronTab(user=True)

# # # 创建任务 指明运行python脚本的命令(crontab的默认执行路径为：当前用户的根路径, 因此需要指定绝对路径)
# # #job = cron_manager.new(command='python /Users/xhl/work/tools/fetch_oms.py >> /Users/xhl/work/tools/logs.log 2>&1 &')
# # job = cron_manager.new(command='python /Users/xhl/work/tools/edit.py >> /Users/xhl/work/tools/logs.log 2>&1 &')

# # # 设置任务执行周期，每两分钟执行一次(更多方式请稍后参见参考链接)
# # job.setall('*/2 * * * *')

# # # 将crontab写入linux系统配置文件
# # my_user_cron.write()
0 1 * * * python /Users/xhl/work/tools/test1.py  /Users/xhl/work/tools/logs.log 2>&1
# # # 0 1 * * * python /path/to/script.py


# # print("helo world")

# # # * * * * * command python /Users/xhl/work/tools/fetch_oms.py /Users/xhl/work/tools/logs.log 2>&1

# # 每两分钟运行一次
# job.minute.every(1) # Set to */1 * * * *