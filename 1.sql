insert overwrite table dw.fy_month_shop_stat_df partition (month_id = '2023-10-18')
select current_timestamp()                           as etl_time       -- etl时间

     , uuid() as row_id         -- 编号


     , if(t2.order_month is not null,t2.order_month,t3.order_month) as order_month    -- 销售月份


     
     , t1.f_company_name                             as f_company_name -- 合同主体-公司名称
     
     , if(t2.order_month is not null,t2.con_shop_code,t3.con_shop_code)  as con_shop_code  -- 铺位号-商铺编码

     , t2.con_shop_name                              as con_shop_name  -- 商铺名称
     , t1.customer_name                              as customer_name  -- 商户名-商户名称
     , t1.brand_name                                 as brand_name     -- 品牌名-品牌名称

     , t2.off_shop_name                              as off_shop_name  -- 线下店铺ID
     , t2.off_shop_id                                as off_shop_id    -- 线下店铺名称

     , t2.shop_id                                    as on_shop_id     -- 线上店铺ID
     , t2.shop_name                                  as on_shop_name   -- 线上店铺名称
     , t2.platform_name                              as platform_name  -- 平台

     , t1.store_id                                   as store_id       -- 门店 ID
     , t1.los_store_id                               as los_store_id   -- 租赁租户 ID

     , t2.on_pay_gmv                                 as on_pay_gmv     -- 本月线上付款GMV
     , t2.on_deal_gmv                                as on_deal_gmv    -- 本月线上成交GMV
     , t2.on_rfd_gmv                                 as on_rfd_gmv     -- 本月线上退款额
     , t2.on_rfd_rate                                as on_rfd_rate    -- 本月线下退款率

     , t3.off_pay_gmv                                as off_pay_gmv    --  本月线下销售额
     , t3.off_deal_gmv                               as off_deal_gmv   --  本月线下结算额
from `tmp.dw_fy_month_shop_stat_df_02` t1   -- 亿高商铺
left join `tmp.dw_fy_month_shop_stat_df_04`      t2 -- 线上店铺
          on t2.con_shop_code = t1.con_shop_code

full join `tmp.dw_fy_month_shop_stat_df_03` t3 -- 数衍 线下数据
          on t2.order_month = t3.order_month
              and t2.con_shop_code = t3.con_shop_code
;