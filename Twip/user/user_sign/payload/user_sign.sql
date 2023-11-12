/*
 Navicat Premium Data Transfer

 Source Server         : sign
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 12/11/2023 12:29:46
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for user_sign
-- ----------------------------
DROP TABLE IF EXISTS "user_sign";
CREATE TABLE "user_sign" (
  "id" text NOT NULL,
  "user_id" text,
  "time" text,
  "sign" text,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
