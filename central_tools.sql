-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: localhost    Database: central_tools
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `central_tools`
--
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `central_tools` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `central_tools`;

--
-- Table structure for table `aps`
--

DROP TABLE IF EXISTS `aps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aps` (
  `customer_id` varchar(100) NOT NULL,
  `allowed_ap` tinyint DEFAULT NULL,
  `ap_deployment_mode` varchar(25) DEFAULT NULL,
  `ap_group` varchar(25) DEFAULT NULL,
  `cluster_id` varchar(100) DEFAULT NULL,
  `controller_name` varchar(100) DEFAULT NULL,
  `current_uplink_inuse` varchar(25) DEFAULT NULL,
  `down_reason` varchar(200) DEFAULT NULL,
  `ethernets` json DEFAULT NULL,
  `firmware_version` varchar(25) DEFAULT NULL,
  `gateway_cluster_id` varchar(200) DEFAULT NULL,
  `gateway_cluster_name` varchar(200) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `ip_address` varchar(25) DEFAULT NULL,
  `labels` json DEFAULT NULL,
  `last_modified` datetime DEFAULT NULL,
  `macaddr` varchar(50) DEFAULT NULL,
  `mesh_role` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `modem_connected` tinyint DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `notes` varchar(200) DEFAULT NULL,
  `public_ip_address` varchar(25) DEFAULT NULL,
  `radios` json DEFAULT NULL,
  `serial` varchar(50) NOT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `subnet_mask` varchar(25) DEFAULT NULL,
  `swarm_id` varchar(100) DEFAULT NULL,
  `swarm_master` tinyint DEFAULT NULL,
  `swarm_name` varchar(100) DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  PRIMARY KEY (`customer_id`,`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `aruba_part_no` varchar(50) DEFAULT NULL,
  `customer_id` varchar(100) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `device_type` varchar(50) DEFAULT NULL,
  `imei` varchar(50) DEFAULT NULL,
  `macaddr` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `serial` varchar(50) NOT NULL,
  `services` json DEFAULT NULL,
  `tier_type` varchar(45) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `configuration_error_status` tinyint DEFAULT NULL,
  `override_status` tinyint DEFAULT NULL,
  `template_name` varchar(100) DEFAULT NULL,
  `template_hash` varchar(50) DEFAULT NULL,
  `template_error_status` tinyint DEFAULT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  `error` tinyint DEFAULT NULL,
  `error_text` varchar(200) DEFAULT NULL,
  `auto_commit_state` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`customer_id`,`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `group_name` varchar(100) NOT NULL,
  `customer_id` varchar(100) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `AOSVersion` varchar(50) DEFAULT NULL,
  `AllowedDevTypes` json DEFAULT NULL,
  `AllowedSwitchTypes` json DEFAULT NULL,
  `APNetworkRole` varchar(25) DEFAULT NULL,
  `architecture` varchar(25) DEFAULT NULL,
  `MonitorOnly` json DEFAULT NULL,
  `GwNetworkRole` varchar(50) DEFAULT NULL,
  `MonitorOnlySwitch` tinyint DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  PRIMARY KEY (`group_name`,`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ports`
--

DROP TABLE IF EXISTS `ports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ports` (
  `serial` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `port_number` varchar(25) NOT NULL,
  `admin_state` varchar(25) DEFAULT NULL,
  `alignment` varchar(25) DEFAULT NULL,
  `allowed_vlan` json DEFAULT NULL,
  `duplex_mode` varchar(25) DEFAULT NULL,
  `has_poe` tinyint DEFAULT NULL,
  `in_errors` int DEFAULT NULL,
  `out_errors` int DEFAULT NULL,
  `intf_state_down_reason` varchar(50) DEFAULT NULL,
  `is_uplink` tinyint DEFAULT NULL,
  `macaddr` varchar(50) DEFAULT NULL,
  `mode` varchar(25) DEFAULT NULL,
  `mux` varchar(25) DEFAULT NULL,
  `oper_state` varchar(25) DEFAULT NULL,
  `phy_type` varchar(25) DEFAULT NULL,
  `poe_state` varchar(25) DEFAULT NULL,
  `port` int DEFAULT NULL,
  `power_consumption` int DEFAULT NULL,
  `rx_usage` bigint DEFAULT NULL,
  `speed` varchar(25) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `trusted` tinyint DEFAULT NULL,
  `tx_usage` bigint DEFAULT NULL,
  `type` varchar(25) DEFAULT NULL,
  `vlan` int DEFAULT NULL,
  `vlan_mode` tinyint DEFAULT NULL,
  `vsx_enabled` tinyint DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  `customer_id` varchar(100) DEFAULT 'bob',
  PRIMARY KEY (`serial`,`port_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sites` (
  `customer_id` varchar(100) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `site_id` varchar(25) NOT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `associated_device_count` int DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `postal_code` varchar(50) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  `online` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`customer_id`,`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `switches`
--

DROP TABLE IF EXISTS `switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `switches` (
  `firmware_version` varchar(25) DEFAULT NULL,
  `group_id` varchar(25) DEFAULT NULL,
  `group_name` varchar(45) DEFAULT NULL,
  `ip_address` varchar(25) DEFAULT NULL,
  `label_ids` json DEFAULT NULL,
  `labels` json DEFAULT NULL,
  `macaddr` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `public_ip_address` varchar(25) DEFAULT NULL,
  `serial` varchar(50) NOT NULL,
  `site_name` varchar(100) DEFAULT NULL,
  `stack_id` varchar(100) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `switch_type` varchar(25) DEFAULT NULL,
  `uplink_ports` json DEFAULT NULL,
  `usage_int` bigint DEFAULT NULL,
  `chassis_type` tinyint DEFAULT NULL,
  `commander_mac` varchar(25) DEFAULT NULL,
  `cpu_utilization` tinyint DEFAULT NULL,
  `default_gateway` varchar(25) DEFAULT NULL,
  `device_mode` tinyint DEFAULT NULL,
  `fan_speed` varchar(10) DEFAULT NULL,
  `max_power` int DEFAULT NULL,
  `mem_free` int DEFAULT NULL,
  `mem_total` int DEFAULT NULL,
  `power_consumption` int DEFAULT NULL,
  `poe_consumption` int DEFAULT NULL,
  `temperature` tinyint DEFAULT NULL,
  `total_clients` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `uptime` bigint DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  `customer_id` varchar(100) DEFAULT 'bob',
  PRIMARY KEY (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `templates`
--

DROP TABLE IF EXISTS `templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `templates` (
  `template_name` varchar(100) NOT NULL,
  `customer_id` varchar(100) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `device_type` varchar(25) DEFAULT NULL,
  `group_name` varchar(100) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `template_hash` varchar(50) DEFAULT NULL,
  `version` varchar(25) DEFAULT NULL,
  `filename` varchar(100) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  PRIMARY KEY (`template_name`,`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test1`
--

DROP TABLE IF EXISTS `test1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test1` (
  `idtest1` int NOT NULL,
  `test1col` varchar(45) DEFAULT NULL,
  `test1col1` varchar(45) DEFAULT NULL,
  `test1col2` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtest1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `variables`
--

DROP TABLE IF EXISTS `variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `variables` (
  `variable_name` varchar(100) NOT NULL,
  `customer_id` varchar(100) NOT NULL,
  `value` varchar(6000) DEFAULT NULL,
  `serial` varchar(50) NOT NULL,
  `last_refreshed` datetime DEFAULT NULL,
  PRIMARY KEY (`variable_name`,`customer_id`,`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Current Database: `central_tools_admin`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `central_tools_admin` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `central_tools_admin`;

DROP TABLE IF EXISTS `home_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `home_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `central_url` varchar(200) NOT NULL,
  `central_custID` varchar(100) NOT NULL,
  `central_clientID` varchar(100) NOT NULL,
  `central_client_secret` varchar(100) NOT NULL,
  `central_token` varchar(100) NOT NULL,
  `central_refresh_token` varchar(100) NOT NULL,
  `user_id` int NOT NULL,
  `central_tokenID` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `home_profile_user_id_5bf46ea0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-04 11:01:11
