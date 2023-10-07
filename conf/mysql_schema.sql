CREATE TABLE `goagoo_bill_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shop_id` varchar(100) DEFAULT NULL COMMENT '数衍平台机构编号',
  `shop_name` varchar(100) DEFAULT NULL COMMENT '数衍平台机构名称',
  `shop_entity_id` varchar(100) DEFAULT NULL COMMENT '数衍平台店铺编号',
  `shop_entity_name` varchar(100) DEFAULT NULL COMMENT '数衍平台店铺名称',
  `sale_time` varchar(100) DEFAULT NULL COMMENT '销售日期（销售时间取年月日）',
  `receivable_amount` varchar(100) DEFAULT NULL COMMENT '当日累计应收确认后金额',
  `remark` varchar(200) DEFAULT NULL COMMENT '备注',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '数衍汇总数据表'