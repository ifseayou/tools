#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/27 17:20:22
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''
from dataclasses import field
from json.tool import main
import re



### 类型映射
def field_transfer(input_str):
    if 'varchar' in input_str:
        return 'string'
    elif 'datetime' in input_str:
        return 'timestamp'
    elif 'int' in input_str:
        return 'bigint'
    elif 'decimal' in input_str:
        return 'double'
    else:
        return 'string' 

def parese_table_comment(table_comment):
    # 使用正则表达式匹配'COMMENT'之后的字符串
    match2 = re.search(r"COMMENT\s*=\s*'([^']*)'", table_comment)

    # 如果找到匹配，则提取评论字符串并去除前后空格
    if match2:
        table_comment = match2.group(1).strip()

    return table_comment
        
def parse_table_name(table_name):
    
    # 使用正则表达式提取字符串
    match1 = re.search(r'CREATE TABLE `([^`]+)`', table_name)
    if match1:
        table_name = match1.group(1)  # 获取匹配到的字符串，并去掉 '`' 符号
        mysql_table_name = table_name
        table_name ="ods_" + data_zone + '_' + table_name + "_df"
    else:
        print("未找到匹配的字符串") 
    return table_name,mysql_table_name

def table_scheme_parse(lines):
    
    table_schema = ''
    table_name = ''
    table_comment = ''
    table_comment = ''

    mysql_table_name = ''

    dsl_sql = ''

    # 标志变量，用于指示是否已经找到表的定义
    found_table = False


    # 遍历文件的每一行
    for line in lines:
        # 如果找到CREATE TABLE行，则将其赋值给table_name并设置found_table标志为True
        if 'CREATE TABLE' in line and not found_table:
            table_name = line.strip()
            mysql_table_name = table_name
            found_table = True

        # 如果已经找到表的定义，并且不包含PRIMARY KEY，则将行添加到 table_schema  中
        elif found_table and 'PRIMARY KEY' not in line and 'ENGINE' not in line :
            
            # 提取注释信息
            match0 = re.search(r"'([^']*)'", line)
            tmp1 = ''
            if match0:
                tmp1 = match0.group(1)
            
            # 使用空格拆分字符串并保留前两个字段
            fields = line.split(None, 2)[:2]

            # 转化数据类型
            field_type =  field_transfer(fields[1])

            # 拼接每一个字段
            tmp_schema = f"{fields[0]} {field_type} comment '{tmp1}', \n"
            
            # 拼接 dsl_sql 语句

            dsl_sql += fields[0]+',\n'

            table_schema += tmp_schema 

        # 如果包含'ENGINE'，则将行赋值给last_line，并且打印它
        elif 'ENGINE' in line:
            table_comment = line

    table_schema += "`etl_time` timestamp comment '数据采集时间' "
    table_name,mysql_table_name = parse_table_name(table_name)
    table_comment = parese_table_comment(table_comment)


    table_sign = f"""
create table if not exists `{table_name}` (
{table_schema}
) comment '{table_comment}'
partitioned by (`date_id` string)
row format delimited fields terminated by '\\001' lines terminated by '\\n'
stored as textfile
;
"""
    print(dsl_sql)

    dsl_sql = f"""
select {dsl_sql}
now() as etl_time
from {mysql_table_name}
;
"""
    print(dsl_sql)

    return table_sign,dsl_sql



if __name__ == '__main__':
    
    # 接收用户输入并赋值给 data_zone，如果用户没有输入则默认为 'live'
    data_zone = input("请输入数据区域（默认为'live'）：") or 'live'

    # 文件路径
    read_file_path = "./conf/mysql_schema.sql"
    write_file_path = "./conf/hive_schema.sql"

    # 打开文件并读取内容
    with open(read_file_path, 'r') as file:
        lines = file.readlines()

    table_sign ,dsl_sql = table_scheme_parse(lines)

    # 打开文件并清空内容，然后写入新字符串
    with open(write_file_path, 'w') as file:
        file.write(table_sign)

        
        file.write("""

            \n
            \n
            \n
        
        """)
    
        file.write(dsl_sql)
