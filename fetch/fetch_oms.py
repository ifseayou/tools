#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/28 10:08:09
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

import os
import schedule
import time

from impala.dbapi import connect
import pandas as pd
from datetime import datetime, timedelta
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



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


def send_email(subject, message, to_email, from_email, password, smtp_server, smtp_port, attachment=None):
    ret=True
    try:
        # 创建一个带附件的邮件对象
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # 添加文本内容
        text = MIMEText(message)
        msg.attach(text)

        # 添加附件
        if attachment:
            part = MIMEApplication(open(attachment, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=attachment)
            msg.attach(part)

        # 连接SMTP服务器并发送邮件
        # server=smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)  
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception:  
        ret=False
    return ret

def get_email_conn():
    # 创建一个ConfigParser对象
    config = configparser.ConfigParser()
    # 读取INI文件
    config.read('../conf/db.ini')
    # 获取特定键的值
    to_email = config.get('oms_email', 'to_email')
    from_email = config.get('oms_email', 'from_email')
    password = config.get('oms_email', 'password')
    smtp_server = "smtp.exmail.qq.com"
    smtp_port = 465
    return to_email,from_email,password,smtp_server,smtp_port


def job():

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
    output_folder = '../output'

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 导出DataFrame到Excel
    output_file = os.path.join(output_folder, f'oms_{yesterday}.xlsx')
    df.to_excel(output_file, index=False)

    print(f"查询结果已导出到 {output_file}")


    # 设置邮箱信息
    to_email,from_email,password,smtp_server,smtp_port = get_email_conn()


    subject = "OMS 清洗数据提取"
    message = "黄老板请注意，数据见email中的Excel，注意数据安全，谨慎使用"

    
    attachment = f'../output/oms_{yesterday}.xlsx'
    
    ret = send_email(subject, message, to_email, from_email, password, smtp_server, smtp_port ,attachment)

    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


if __name__ == '__main__':

    schedule.every().friday.at("08:31").do(job) 
    while True:
        schedule.run_pending()   # 运行所有可以运行的任务
        time.sleep(1)
