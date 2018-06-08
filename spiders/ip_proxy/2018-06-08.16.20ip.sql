-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.21 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出  表 ip_proxy.ip 结构
CREATE TABLE IF NOT EXISTS `ip` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `ip` bigint(20) DEFAULT NULL COMMENT 'ip地址',
  `type` tinyint(4) unsigned DEFAULT NULL COMMENT 'ip类型',
  `port` int(10) unsigned DEFAULT NULL COMMENT '端口',
  `isp` varchar(50) DEFAULT NULL COMMENT '运营商',
  `country` varchar(50) DEFAULT NULL COMMENT '国家',
  `region` varchar(50) DEFAULT NULL COMMENT '省',
  `city` varchar(50) DEFAULT NULL COMMENT '城市',
  `area` varchar(50) DEFAULT NULL COMMENT '地区',
  `status` tinyint(4) DEFAULT '1' COMMENT '状态',
  `create_time` double unsigned DEFAULT NULL COMMENT '捕获时间',
  `update_time` double unsigned DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Ip列表';

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
