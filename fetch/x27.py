#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/11/08 17:15:29
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''


import pandas as pd
from fetch_oms import get_impala_conn


file_path = '/Users/xhl/work/tools/input/X27样品清单_11.7.xlsx'
df1 = pd.read_excel(file_path,sheet_name='库位库存批量导出_1')
# print(df1)


query = f"""
select t1.sku_code     as sku_code
     , max(brand_name) as brand_name
from dwd.goods_item_sku_di  t1
left join dwd.goods_item_di t2
          on t1.item_no = t2.item_no
              and t2.date_id = '2023-11-07'
              and t2.is_deleted = '0'
where t1.date_id = '2023-11-07'
  and t1.is_deleted = 0
group by t1.sku_code
"""

print(query)
conn = get_impala_conn()


refresh1 = 'refresh dwd.goods_item_di;'
refresh2 = 'refresh dwd.goods_item_sku_di;'

conn = get_impala_conn()

# 连接到Impala


cursor = conn.cursor()
cursor.execute(refresh1)
cursor.execute(refresh2)


df2 = pd.read_sql(query, conn)

print('fetch data ing....')
conn.close()


dfx = pd.merge(df1, df2, left_on=['商品条码'], right_on=['sku_code'], how='left')
print('join ing')

dfx.to_excel('./output/output.xlsx', index=False)


# selected_column = '商品条码'  # 选择需要处理的列
# column_series = ", ".join(df1[selected_column].apply(lambda x: f"'{x}'"))


# 打印结果
# with open('/Users/xhl/work/tools/fetch/output/code.txt', 'w') as file:  # 覆盖写入
#     file.write(column_series)


# print(column_series)



# yesterday = get_yesterday()






计算机中的三个周期：时钟周期：即为计算机主频；CPU周期：从内存里读取一条指令的最短时间；；指令周期：一条指令的执行需要的几个步骤。取指令-指令译码-指令执行
CPU周期包含多个时钟周期，一个指令周期包含多个CPU周期

