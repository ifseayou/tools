#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/08 10:33:06
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

import pandas as pd
import os
from fetch_oms import get_impala_conn,get_yesterday,get_email_conn,send_email
import warnings
warnings.filterwarnings("ignore")


def read_excel_write_excel(file_path):
    df = pd.read_excel(file_path,sheet_name='Sheet1')
    row_cnt = df.shape[0]

    # df = df.iloc[1:,0]
    # df = df[['订单号']]
    df = df['订单号'].astype(str).apply(lambda x: f"'{x}'")
    # print(df)
    # 使用逗号拼接所有字符串
    order_nos = ','.join(df)
    # print(row_cnt)
    
    # return order_nos, row_cnt

# def get_rfd_order(order_nos):
    yesterday = get_yesterday()
    refresh1 = 'refresh  dw.fna_order_goods_df'
    conn = get_impala_conn()
    # 连接到Impala
    cursor = conn.cursor()
    cursor.execute(refresh1)

    query = f"""
select order_no as '订单编号'
     , deal_amt as '订单价格'
     , order_status_name as '订单状态'

     , order_created_at as '下单时间'
     , payment_at as '付款时间'
     , platform_name as '媒体平台'
     , order_from_name as '商品平台'
     , anchor_nick as '主播昵称'
     , goods_name as '商品名称'
     , goods_id as '商品ID'
     , purchaser_name as '招商'
     , supplier_id as '供应商ID'
     , supplier_name as '供应商名称'
     , yw_goods_id '遥望云商品id'
     , goods_num as '播品数量'
     , shop_name as '店铺名称'
     , shop_id as '店铺ID'
     , settlement_biz_type as '订单类型'
     , warehouse_name as '发货仓'
from dw.fna_order_goods_df
where order_no in ({order_nos})
"""

    # print(query)


    # 执行查询并将结果存储在DataFrame中
    df = pd.read_sql(query, conn)

    # 关闭Impala连接
    conn.close()

    # 目标Excel文件夹
    output_folder = '/Users/xhl/work/tools/fetch/output'

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 导出DataFrame到Excel
    output_file = os.path.join(output_folder, f'rfd_order_{yesterday}.xlsx')
    df.to_excel(output_file, index=False)

    print(f"查询结果已导出到 {output_file}")


if __name__ == '__main__':
    
    file_path = '/Users/xhl/work/tools/input/订单数据.xlsx'
    
    read_excel_write_excel(file_path)

    to_email,from_email,password,smtp_server,smtp_port = get_email_conn()
    to_email = 'lingcui@ywwl.com'


    yesterday = get_yesterday()
    subject = f"莹莹_{yesterday}_客服月度赔付"
    message = "数据见email中的Excel"
    
    attachment = f'/Users/xhl/work/tools/fetch/output/rfd_order_{yesterday}.xlsx'
    
    ret = send_email(subject, message, to_email, from_email, password, smtp_server, smtp_port ,attachment)

    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
