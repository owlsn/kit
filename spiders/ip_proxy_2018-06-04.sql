# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 119.27.170.185 (MySQL 5.7.22-0ubuntu0.16.04.1)
# Database: ip_proxy
# Generation Time: 2018-06-04 12:31:38 +0000
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
  `ip` bigint(20) unsigned DEFAULT NULL COMMENT 'ip地址',
  `create_time` int(10) unsigned DEFAULT NULL COMMENT '插入时间',
  `update_time` int(11) unsigned DEFAULT NULL COMMENT '验证时间',
  `operator` varchar(50) DEFAULT NULL COMMENT '运营商',
  `area` varchar(50) DEFAULT NULL COMMENT '代理地区',
  `type` tinyint(4) unsigned DEFAULT NULL COMMENT 'ip类型',
  `port` int(10) unsigned DEFAULT NULL COMMENT '端口',
  PRIMARY KEY (`id`),
  KEY `ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Ip列表';



# Dump of table stratigy
# ------------------------------------------------------------

DROP TABLE IF EXISTS `stratigy`;

CREATE TABLE `stratigy` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` tinyint(3) unsigned DEFAULT NULL COMMENT '类型',
  `url` varchar(255) DEFAULT NULL COMMENT 'url',
  `create_time` int(10) unsigned DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='检测策略';




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
