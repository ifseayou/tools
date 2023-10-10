#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/08 14:30:41
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

import datetime
import pandas as pd
import os
from fetch_oms import get_impala_conn,get_yesterday,get_email_conn,send_email

def query_download():

    yesterday = get_yesterday()
    refresh1 = 'refresh  app.bi_account_date_goods_source_df'
    refresh2 = 'refresh  dim.goods_spu_df'
    refresh3 = 'refresh  dim.live_purchaser_da'
    conn = get_impala_conn()
    # 连接到Impala
    cursor = conn.cursor()
    cursor.execute(refresh1)
    cursor.execute(refresh2)
    cursor.execute(refresh3)

    today = datetime.date.today()
    month_first_day = today.replace(day=1)

    query = f"""
select substr(t1.nn_order_date, 1, 7)                                                                 as `月份`
     , t2.brand                                                                                       as `品牌`
     , t3.main_dept4_name                                                                             as `直播部门`
     , t2.purchaser_name                                                                              as `行业运营`
     , sum(t1.deal_sales_amt)                                                                         as `有效GMV`
     , sum(t1.total_gross_profit)                                                                     as `商品总毛利`
     , sum(t1.order_online_commission)                                                                as `线上预估总佣金`
     , sum(case when t1.flow_source_tag_id in ('0110', '0210') then t1.offline_repair_commission end) as `提报线下补佣`
     , sum(case when t1.flow_source_tag_id in ('0110', '0210') then t1.guarantee_commission end)      as `提报保比佣金`
     , sum(t1.shop_gross_profit)                                                                      as `小店毛利额`
     , sum(case when t1.flow_source_tag_id in ('0110', '0210') then t1.pit_fee end)                   as `品牌坑位费`
from (select nn_order_date
           , brand_name
           , dept_name
           , purchaser_name
           , yw_goods_id
           , flow_source_tag_id
           , deal_sales_amt
           , total_gross_profit
           , order_online_commission
           , offline_repair_commission
           , guarantee_commission
           , shop_gross_profit
           , pit_fee
      from app.bi_account_date_goods_source_df
      where nn_order_date < '{month_first_day}'
        and nn_order_date >= '2022-01-01'
)                               t1
left join dim.goods_spu_df      t2
          on t1.yw_goods_id = t2.yw_goods_id
left join dim.live_purchaser_da t3
          on t2.purchaser_id = t3.purchaser_id
                 and t3.date_id = '{yesterday}'
group by substr(t1.nn_order_date, 1, 7)
       , t2.brand
       , t3.main_dept4_name
       , t2.purchaser_name
"""

    # print(query)
    
    # 执行查询并将结果存储在DataFrame中
    df = pd.read_sql(query, conn)

    # 关闭Impala连接
    conn.close()

    # 目标Excel文件夹
    output_folder = '../output'

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 导出DataFrame到Excel
    output_file = os.path.join(output_folder, f'brand_33_{yesterday}.xlsx')
    df.to_excel(output_file, index=False)

    print(f"查询结果已导出到 {output_file}")


if __name__ == '__main__':
    

    query_download()


    to_email,from_email,password,smtp_server,smtp_port = get_email_conn()
    to_email = 'lingcui@ywwl.com'

    yesterday = get_yesterday()
    subject = f"得久_{yesterday}_行业运营品牌基础销售值"
    message = "数据见email中的Excel"
    
    attachment = f'../output/brand_33_{yesterday}.xlsx'
    
    ret = send_email(subject, message, to_email, from_email, password, smtp_server, smtp_port ,attachment)

    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
