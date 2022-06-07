-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: central_tools_admin
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(50) NOT NULL,
  `menu_url` varchar(300) NOT NULL,
  `group_id` int DEFAULT NULL,
  `menu_type` int NOT NULL,
  `menu_parent_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menus_group_id_be5585e6_fk_auth_group_id` (`group_id`),
  KEY `menus_menu_parent_id_9441c8b9_fk_menus_id` (`menu_parent_id`),
  CONSTRAINT `menus_group_id_be5585e6_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `menus_menu_parent_id_9441c8b9_fk_menus_id` FOREIGN KEY (`menu_parent_id`) REFERENCES `menus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus`
--

LOCK TABLES `menus` WRITE;
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` VALUES (2,'Section 9','/',NULL,3,NULL),(3,'Motoko Kusanagi','/',NULL,1,2),(4,'Batou','/',NULL,1,2),(5,'Togusa','/',NULL,1,2),(6,'Ishikawa','/',NULL,1,2),(7,'Pazu','/',NULL,1,2),(8,'Boma','/',NULL,1,2),(9,'Saito','/',NULL,1,2),(10,'Tachikoma','/',NULL,1,3),(11,'Babylon 5','/',1,3,NULL),(12,'John Sheridan','/',NULL,1,11),(20,'Michael Garibaldi','/security/',NULL,1,12),(21,'Susan Ivanova','/',3,1,12),(22,'Operations','/',NULL,3,12),(24,'Tasks','/',1,3,NULL),(25,'Create Template Group & Upload Templatee','create_tgroup/',NULL,1,24),(26,'Create Multi TG and Upload Template','create_mtgroup/',NULL,1,24),(27,'Show Sites','show_sites/',NULL,1,24),(28,'Update Vars','WF1select_site/',NULL,1,24),(29,'Device Config','WFcfg_select_site/',NULL,1,24),(30,'Zocolo','/',NULL,3,11),(31,'Jack\'s Used Ships','/',NULL,1,30),(32,'SQL Query','WFsql/',NULL,1,24);
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-07 23:53:26
