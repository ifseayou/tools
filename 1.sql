    select sum(case when order_status_name = '已支付' then charge_amt else 0 end)               as charge_amt    -- 充值流水
         , sum(case when order_status_name = '已支付' then charge_amt * divide_rate else 0 end) as charge_income -- 流水收入
         , count(distinct user_id)                                                              as user_cnt      -- 用户数量
    from public.dwd_kudu_short_drama_order_mii
    where substr(order_created_at, 1, 10) >= '2023-10-01'
      and substr(order_created_at, 1, 10) <= '2023-10-25'
      and platform_name in ('常读')
    --   and optimizer_name in ([DYNAMIC_PARAMS.optimizer_name_list])
    --   and drama_name in ([DYNAMIC_PARAMS.drama_name_list])