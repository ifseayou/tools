#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/28 10:08:09
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''


import os
from impala.dbapi import connect
import pandas as pd
from datetime import datetime, timedelta
import configparser



def get_yesterday():
    # 获取当前日期
    current_date = datetime.now()

    # 计算昨天的日期
    yesterday_date = current_date - timedelta(days=1)

    # 格式化日期为字符串（可选）
    yesterday = yesterday_date.strftime("%Y-%m-%d")

    return  yesterday



def get_impala_conn():

    # 创建一个ConfigParser对象
    config = configparser.ConfigParser()
    # 读取INI文件
    config.read('conf/db.ini')
    # 获取特定键的值
    impala_host = config.get('impala_conf', 'impala_host')
    impala_port = int(config.get('impala_conf', 'impala_port'))
    impala_user = config.get('impala_conf', 'impala_user')
    
    return connect(host=impala_host, port=impala_port, user=impala_user)
    


if __name__ == '__main__':

    yesterday = get_yesterday()

    # 查询语句
    query = f"""
    with tmp1 as ( --
        select *
        from ( --
            select *
                , row_number() over(partition by platform_as_goods_code order by u_time desc ) as rn
            from ods.oms_excel_clean_df
            where date_id = '{yesterday}'
        ) t
        where rn = 1
        and status = 'WaitConfirm'
    )
    , tmp2 as ( --

        select  etl_time
            , upload_date
            , pk_id
            , person_type_id
            , person_type_name
            , from_tag
            , platform_as_code
            , platform_as_goods_code
            , sku_id
            , qty
            , price
            , amount
            , sku_refund
            , sku_name
            , pic
            , coalesce(if(t1.type = '', null ,t1.type),t2.type,t3.type) as type
            , properties_value
            , return_qty
            , created_at
            , updated_at
            , platform_order_no
            , cq_after_sale_no
            , outer_order_no
            , supplier_id
            , vc_name
            , after_sale_at_num
            , after_sale_at
            , outer_as_id
            , modified
            , status
            , good_status
            , question_type
            , warehouse_name
            , refund
            , payment
            , shop_buyer_id
            , shop_id
            , shop_name
            , receiver_name
            , logistics_company_name
            , express_no
            , warehouse_id
            , created_at_from_order
            , updated_at_from_order
            , buyer_remark
            , seller_remark
            , person_tag
            , creator
            , editor
            , c_time
            , u_time
            , date_id
            , rn
        from tmp1   t1
        left join ( --
                    select after_sale_no

                        , case
                                when after_sale_type = '1' then '仅退款'
                                when after_sale_type = '2' then '退货退款'
                                when after_sale_type = '3' then '换货'
                                when after_sale_type = '4' then '补发'
                                when after_sale_type = '5' then '赔偿'
                                when after_sale_type = '6' then '退货' end as type
                    from ods.oms_customer_after_sale_main_df
                    where date_id = '{yesterday}'
                ) t2
                on t1.platform_as_code = t2.after_sale_no
        left join (select after_sale_no
                        , case
                            when aftersale_type = '1' then '仅退款'
                            when aftersale_type = '2' then '退货退款'
                            when aftersale_type = '3' then '维修'
                            when aftersale_type = '4' then '换货'
                            when aftersale_type = '5' then '补寄'
                            when aftersale_type = '6' then '保价'
                            when aftersale_type = '7' then '系统取消'
                            when aftersale_type = '8' then '用户取消' end as type

                from ods.oms_customer_self_after_sale_order_df
                where date_id = '{yesterday}'
                ) t3
        on t1.platform_as_code = t3.after_sale_no
    )

    select etl_time
            , upload_date
            , pk_id
            , person_type_id
            , person_type_name
            , from_tag
            , platform_as_code
            , platform_as_goods_code
            , sku_id
            , qty
            , price
            , amount
            , sku_refund
            , sku_name
            , pic
            , type
            , properties_value
            , return_qty
            , created_at
            , updated_at
            , platform_order_no
            , cq_after_sale_no
            , outer_order_no
            , supplier_id
            , vc_name
            , after_sale_at_num
            , after_sale_at
            , outer_as_id
            , modified
            , status
            , good_status
            , question_type
            , warehouse_name
            , refund
            , payment
            , shop_buyer_id
            , shop_id
            , shop_name
            , receiver_name
            , logistics_company_name
            , express_no
            , warehouse_id
            , created_at_from_order
            , updated_at_from_order
            , buyer_remark
            , seller_remark
            , person_tag
            , creator
            , editor
            , c_time
            , u_time
            , date_id
            , rn
    from tmp2
    """


    refresh1 = 'refresh ods.oms_excel_clean_df;'
    refresh2 = 'refresh ods.oms_customer_after_sale_main_df;'
    refresh3 = 'refresh ods.oms_customer_self_after_sale_order_df;'

    conn = get_impala_conn()

    # 连接到Impala


    cursor = conn.cursor()
    cursor.execute(refresh1)
    cursor.execute(refresh2)
    cursor.execute(refresh3)


    # 执行查询并将结果存储在DataFrame中
    df = pd.read_sql(query, conn)

    # 关闭Impala连接
    conn.close()

    # 目标Excel文件夹
    output_folder = './output'

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 导出DataFrame到Excel
    output_file = os.path.join(output_folder, f'oms_{yesterday}.xlsx')
    df.to_excel(output_file, index=False)

    print(f"查询结果已导出到 {output_file}")
