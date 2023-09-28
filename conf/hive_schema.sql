
create table if not exists `ods_live_goagoo_bill_report_df` (
`id` bigint comment '', 
`shop_id` string comment '数衍平台机构编号', 
`shop_name` string comment '数衍平台机构名称', 
`shop_entity_id` string comment '数衍平台店铺编号', 
`shop_entity_name` string comment '数衍平台店铺名称', 
`sale_time` string comment '销售日期（销售时间取年月日）', 
`receivable_amount` string comment '当日累计应收确认后金额', 
`remark` string comment '备注', 
`updated_at` timestamp comment '更新时间', 
`created_at` timestamp comment '创建时间', 
`etl_time` timestamp comment '数据采集时间' 
) comment '数衍汇总数据表'
partitioned by (`date_id` string)
row format delimited fields terminated by '\001' lines terminated by '\n'
stored as textfile
;


        
select `id`,
`shop_id`,
`shop_name`,
`shop_entity_id`,
`shop_entity_name`,
`sale_time`,
`receivable_amount`,
`remark`,
`updated_at`,
`created_at`,

now() as etl_time
from goagoo_bill_report
;