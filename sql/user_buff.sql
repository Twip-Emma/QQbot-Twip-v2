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

 Date: 29/08/2023 14:38:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_buff
-- ----------------------------
DROP TABLE IF EXISTS `user_buff`;
CREATE TABLE `user_buff`  (
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `buff_1` int NULL DEFAULT NULL,
  `buff_2` int NULL DEFAULT NULL,
  `buff_3` int NULL DEFAULT NULL,
  `buff_4` int NULL DEFAULT NULL,
  `buff_5` int NULL DEFAULT NULL,
  `buff_6` int NULL DEFAULT NULL,
  `buff_7` int NULL DEFAULT NULL,
  `buff_8` int NULL DEFAULT NULL
) ENGINE = InnoDB AUTO_INCREMENT = 168 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
