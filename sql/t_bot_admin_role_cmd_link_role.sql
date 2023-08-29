/*
 Navicat Premium Data Transfer

 Source Server         : 云数据库-qqbot-分区1
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : rm-8vbu4rkgv70eqp2y50o.mysql.zhangbei.rds.aliyuncs.com:3306
 Source Schema         : qqbot-twip-database-1

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 29/08/2023 14:37:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_bot_admin_role_cmd_link_role
-- ----------------------------
DROP TABLE IF EXISTS `t_bot_admin_role_cmd_link_role`;
CREATE TABLE `t_bot_admin_role_cmd_link_role`  (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cmd_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '命令ID',
  `role_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
