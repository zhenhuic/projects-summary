/*
 Navicat Premium Data Transfer

 Source Server         : pujiangpanshao
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 26/05/2020 12:30:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for process_record
-- ----------------------------
DROP TABLE IF EXISTS `process_record`;
CREATE TABLE `process_record`  (
  `date_record` datetime(0) NULL DEFAULT NULL,
  `xiaobaozujian_get` int(255) NULL DEFAULT NULL,
  `fengguan_get` int(255) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
