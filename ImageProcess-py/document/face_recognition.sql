/*
Navicat MySQL Data Transfer

Source Server         : localhost_mysql
Source Server Version : 80013
Source Host           : localhost:3306
Source Database       : face_recognition

Target Server Type    : MYSQL
Target Server Version : 80013
File Encoding         : 65001

Date: 2019-11-08 14:38:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for blacklist
-- ----------------------------
DROP TABLE IF EXISTS `blacklist`;
CREATE TABLE `blacklist` (
  `id` varchar(36) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(100) NOT NULL,
  `memo` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for record
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record` (
  `id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `frame` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `recognizedAt` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `camera` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `location` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;