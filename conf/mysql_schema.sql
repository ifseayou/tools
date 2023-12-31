CREATE TABLE `order_goods_1_0` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `platform_order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '平台订单编号',
  `goods_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '商品ID',
  `goods_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商品名称',
  `goods_price` int NOT NULL DEFAULT '0' COMMENT '商品单价',
  `goods_num` int NOT NULL DEFAULT '0' COMMENT '商品数量',
  `goods_img` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商品图片',
  `shop_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '店铺名称',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `cat1_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '一级类目ID',
  `cat1_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '一级类目名称',
  `combo_sku_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '组合sku编码',
  `sku_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'sku名称',
  `sale_user_nick` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '销售昵称',
  `pk_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '主键id',
  `gift_num` int DEFAULT NULL COMMENT '赠品数量',
  `shop_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '店铺ID',
  `order_created_at` datetime(3) DEFAULT NULL COMMENT '下单时间',
  `platform` int NOT NULL COMMENT '平台：1:快手 2:抖音 3:小红书 4:B站 5:淘宝 6:微博\n7:西瓜 9:火山',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '删除标记（0：未删除；1：已删除）',
  `sku_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '商品SkuId',
  `goods_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '商品链接',
  `original_price` int NOT NULL DEFAULT '0' COMMENT '商品促销前单价',
  `discount_price` int NOT NULL DEFAULT '0' COMMENT '折扣金额',
  `item_total_amount` int NOT NULL DEFAULT '0' COMMENT '优惠前订单明细总金额',
  `shop_discount_amount` int NOT NULL DEFAULT '0' COMMENT '明细级商家承担优惠金额',
  `platform_discount_amount` int NOT NULL DEFAULT '0' COMMENT '明细级平台优惠金额',
  `talent_discount_amount` int NOT NULL DEFAULT '0' COMMENT '明细级主播优惠金额',
  `oid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '商品子单oid',
  `refund_status` int NOT NULL DEFAULT '0' COMMENT '退款状态 0未退款 10退款中 30 退款完成 40 退款关闭',
  `third_party_shop_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '三方店铺Id',
  PRIMARY KEY (`id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_order_created_at` (`order_created_at`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_platform_order_created_at_platform` (`platform_order_no`,`order_created_at`,`platform`
  ) USING BTREE COMMENT '订单号+下单时间+媒体平台联合索引'
) ENGINE = InnoDB AUTO_INCREMENT = 935249 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '订单商品表|订单管理|方腊'