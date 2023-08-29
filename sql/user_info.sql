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

 Date: 29/08/2023 14:38:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `user_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `last_speak_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `speak_time_total` int NULL DEFAULT NULL,
  `coin` double NULL DEFAULT NULL
) ENGINE = InnoDB AUTO_INCREMENT = 30114 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
