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

 Date: 19/05/2020 12:34:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zhuangxiang
-- ----------------------------
DROP TABLE IF EXISTS `zhuangxiang`;
CREATE TABLE `zhuangxiang`  (
  `date` datetime(0) NOT NULL,
  `zhuagnxiang_id` int(11) NULL DEFAULT NULL,
  `kaishizhuagnxiang` int(11) NULL DEFAULT NULL,
  `jieshuzhuagnxiang` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of zhuangxiang
-- ----------------------------
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:28:38', 1, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:29:11', 1, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:29:15', 2, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:29:53', 2, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:29:57', 3, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:30:30', 3, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:30:34', 4, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:31:37', 4, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:31:42', 5, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:32:12', 5, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:32:16', 6, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:32:50', 6, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:32:54', 7, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:34:09', 7, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:34:13', 8, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:34:48', 8, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:34:52', 9, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:36:08', 9, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:36:13', 10, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:36:41', 10, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:36:45', 11, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:37:17', 11, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:37:22', 12, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:37:53', 12, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:37:57', 13, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:38:27', 13, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:38:31', 14, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:39:13', 14, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:39:18', 15, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:39:46', 15, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:39:50', 16, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:40:20', 16, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:40:24', 17, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:40:55', 17, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:40:59', 18, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:41:31', 18, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:41:36', 19, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 11:42:12', 19, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:31:16', 1, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:31:50', 1, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:31:54', 2, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:32:32', 2, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:32:36', 3, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:33:10', 3, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:33:14', 4, 1, 0);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:34:18', 4, 0, 1);
INSERT INTO `zhuangxiang` VALUES ('2020-05-19 12:34:23', 5, 1, 0);

SET FOREIGN_KEY_CHECKS = 1;
