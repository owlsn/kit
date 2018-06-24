# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.22)
# Database: ip_proxy
# Generation Time: 2018-06-14 13:22:36 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table ip
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ip`;

CREATE TABLE `ip` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ip` bigint(20) DEFAULT NULL COMMENT 'ip地址',
  `type` tinyint(4) unsigned DEFAULT NULL COMMENT 'ip类型',
  `scheme` varchar(11) DEFAULT 'http' COMMENT '协议',
  `port` int(10) unsigned DEFAULT NULL COMMENT '端口',
  `isp` varchar(50) DEFAULT NULL COMMENT '运营商',
  `country` varchar(50) DEFAULT NULL COMMENT '国家',
  `region` varchar(50) DEFAULT NULL COMMENT '省',
  `city` varchar(50) DEFAULT NULL COMMENT '城市',
  `area` varchar(50) DEFAULT NULL COMMENT '地区',
  `status` tinyint(4) DEFAULT '1' COMMENT '状态',
  `create_time` double unsigned DEFAULT NULL COMMENT '捕获时间',
  `update_time` double unsigned DEFAULT NULL COMMENT '更新时间',
  `level` int(10) DEFAULT '0' COMMENT '检测优先级',
  `delay` int(11) DEFAULT '-1' COMMENT '延时',
  `flag` tinyint(4) DEFAULT 0 COMMENT '是否查询ip地址信息',
  `source` VARCHAR(50) NULL DEFAULT NULL COMMENT 'ip来源',
  `times` int(11) unsigned DEFAULT '0' COMMENT '失效次数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Ip列表';




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
