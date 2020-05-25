/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : intrusion_detection

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 25/05/2020 10:43:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for baobantongyong
-- ----------------------------
DROP TABLE IF EXISTS `baobantongyong`;
CREATE TABLE `baobantongyong`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of baobantongyong
-- ----------------------------
INSERT INTO `baobantongyong` VALUES (1, '2020-05-20 16:28:53');
INSERT INTO `baobantongyong` VALUES (2, '2020-05-20 16:30:04');
INSERT INTO `baobantongyong` VALUES (3, '2020-05-20 16:31:06');
INSERT INTO `baobantongyong` VALUES (4, '2020-05-21 19:23:23');
INSERT INTO `baobantongyong` VALUES (5, '2020-05-20 19:23:29');
INSERT INTO `baobantongyong` VALUES (6, '2020-05-20 19:23:36');
INSERT INTO `baobantongyong` VALUES (7, '2020-05-21 19:23:49');
INSERT INTO `baobantongyong` VALUES (8, '2020-05-21 19:23:55');
INSERT INTO `baobantongyong` VALUES (9, '2020-05-21 19:24:02');

-- ----------------------------
-- Table structure for penfenshang
-- ----------------------------
DROP TABLE IF EXISTS `penfenshang`;
CREATE TABLE `penfenshang`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of penfenshang
-- ----------------------------
INSERT INTO `penfenshang` VALUES (1, '2020-05-20 16:34:48');
INSERT INTO `penfenshang` VALUES (2, '2020-05-20 16:35:49');
INSERT INTO `penfenshang` VALUES (3, '2020-05-20 16:36:50');
INSERT INTO `penfenshang` VALUES (4, '2020-05-20 16:37:56');
INSERT INTO `penfenshang` VALUES (5, '2020-05-20 16:38:57');
INSERT INTO `penfenshang` VALUES (6, '2020-05-19 19:24:14');
INSERT INTO `penfenshang` VALUES (7, '2020-05-18 19:24:21');
INSERT INTO `penfenshang` VALUES (8, '2020-05-18 19:24:27');

-- ----------------------------
-- Table structure for sawanini_1
-- ----------------------------
DROP TABLE IF EXISTS `sawanini_1`;
CREATE TABLE `sawanini_1`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sawanini_1
-- ----------------------------
INSERT INTO `sawanini_1` VALUES (1, '2020-05-20 19:24:35');
INSERT INTO `sawanini_1` VALUES (2, '2020-05-18 19:24:41');
INSERT INTO `sawanini_1` VALUES (3, '2020-05-17 19:24:47');
INSERT INTO `sawanini_1` VALUES (4, '2020-05-08 19:24:54');
INSERT INTO `sawanini_1` VALUES (5, '2020-05-24 19:25:00');
INSERT INTO `sawanini_1` VALUES (6, '2020-05-18 19:25:16');
INSERT INTO `sawanini_1` VALUES (7, '2020-05-19 19:25:27');

-- ----------------------------
-- Table structure for sawanini_2
-- ----------------------------
DROP TABLE IF EXISTS `sawanini_2`;
CREATE TABLE `sawanini_2`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sawanini_2
-- ----------------------------
INSERT INTO `sawanini_2` VALUES (1, '2020-05-11 19:27:53');
INSERT INTO `sawanini_2` VALUES (2, '2020-05-09 19:28:02');
INSERT INTO `sawanini_2` VALUES (3, '2020-05-09 19:28:15');
INSERT INTO `sawanini_2` VALUES (4, '2020-05-10 19:28:21');
INSERT INTO `sawanini_2` VALUES (5, '2020-05-11 19:28:26');
INSERT INTO `sawanini_2` VALUES (6, '2020-05-21 19:28:32');
INSERT INTO `sawanini_2` VALUES (7, '2020-05-08 19:28:45');
INSERT INTO `sawanini_2` VALUES (8, '2020-05-12 19:28:53');

-- ----------------------------
-- Table structure for zhuanjixia
-- ----------------------------
DROP TABLE IF EXISTS `zhuanjixia`;
CREATE TABLE `zhuanjixia`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of zhuanjixia
-- ----------------------------
INSERT INTO `zhuanjixia` VALUES (1, '2020-05-21 19:40:25');
INSERT INTO `zhuanjixia` VALUES (2, '2020-05-07 19:40:33');
INSERT INTO `zhuanjixia` VALUES (3, '2020-05-12 19:40:45');
INSERT INTO `zhuanjixia` VALUES (4, '2020-05-12 19:40:52');
INSERT INTO `zhuanjixia` VALUES (5, '2020-05-13 19:41:00');
INSERT INTO `zhuanjixia` VALUES (6, '2020-05-14 19:41:05');
INSERT INTO `zhuanjixia` VALUES (7, '2020-05-22 19:41:10');
INSERT INTO `zhuanjixia` VALUES (8, '2020-05-16 19:41:16');
INSERT INTO `zhuanjixia` VALUES (9, '2020-05-19 19:41:26');

SET FOREIGN_KEY_CHECKS = 1;
