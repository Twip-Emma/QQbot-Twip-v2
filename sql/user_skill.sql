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

 Date: 29/08/2023 14:39:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_skill
-- ----------------------------
DROP TABLE IF EXISTS `user_skill`;
CREATE TABLE `user_skill`  (
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_mp` int NULL DEFAULT NULL,
  `user_str` int NULL DEFAULT NULL,
  `user_int` int NULL DEFAULT NULL,
  `skill_1` int NULL DEFAULT NULL,
  `skill_2` int NULL DEFAULT NULL,
  `skill_3` int NULL DEFAULT NULL,
  `skill_4` int NULL DEFAULT NULL,
  `skill_5` int NULL DEFAULT NULL,
  `skill_6` int NULL DEFAULT NULL,
  `skill_7` int NULL DEFAULT NULL,
  `skill_8` int NULL DEFAULT NULL
) ENGINE = InnoDB AUTO_INCREMENT = 115 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
