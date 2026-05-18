-- MySQL dump 10.13  Distrib 8.0.46, for macos15 (x86_64)
--
-- Host: localhost    Database: birthday_management_system
-- ------------------------------------------------------
-- Server version	9.6.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '74b0bd0e-508f-11f1-958d-efd66268e542:1-166';

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('manager','member') DEFAULT 'member',
  `selected_birthdays` json DEFAULT (_utf8mb4'[]'),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (11,'birthdaymanager','thevinchi007@gmail.com','scrypt:32768:8:1$0w4S9NjiyO2FgzGM$c5f0007cc6796ef17c53f8cfb26949dbb57a0092d895bfeb9823de3424245daece4cdfb4a8161b4edba4756445a14ab4a6b8b72c7c4501ecf46cd71d2da7ae56','manager','[]'),(13,'U1','demo03gorgan@gmail.com','scrypt:32768:8:1$SFZk7eV6XGZYMe3i$d9836696766c4e6a4fe71926d609824e13acf789759dde81675860a42b41a6abebb69113eb540c19bb7e2a1efb1c9dbe0345856bff2f0ebdc5559e3df2887fa3','member','[3, 4]');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `birthdays`
--

DROP TABLE IF EXISTS `birthdays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `birthdays` (
  `Sl_no` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Batch` varchar(50) DEFAULT NULL,
  `dob` date NOT NULL,
  PRIMARY KEY (`Sl_no`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `birthdays`
--

LOCK TABLES `birthdays` WRITE;
/*!40000 ALTER TABLE `birthdays` DISABLE KEYS */;
INSERT INTO `birthdays` VALUES (1,'priyanshi','y24','2007-03-03'),(2,'tina','y28','2010-10-18'),(4,'Sachin','Y21','2000-01-07'),(5,'Amrendra','PHD','2000-01-15'),(6,'Lakshmi','Y21','2000-01-16'),(7,'Sujal Kumar Sahani','Y25','2000-01-16'),(8,'Alok','Y23','2000-01-19'),(9,'Anish yadav','Y25','2000-01-29'),(10,'Padma A','Y21','2000-01-30'),(11,'Akanksha','Y19','2000-02-01'),(12,'Samar','Y24','2000-02-03'),(13,'Bharat','Y22','2000-02-04'),(14,'Kharte','Y21','2000-02-08'),(15,'Shivam Meena','Y23','2000-02-09'),(16,'Amimay Pandey','Y25','2000-02-10'),(17,'Gaurav Swarnkar','Y24','2000-02-19'),(18,'Abhishek Kumar','Y23','2000-02-29'),(19,'Priyanshi Meena','Y24','2000-03-03'),(20,'Deepak Shankar Jorwal','Y14','2000-03-03'),(21,'Devyani','Y24','2000-03-05'),(22,'Yash Hatwar','Y21','2000-03-06'),(23,'Sahil','Y25','2000-03-10'),(24,'Sahil Kumawat','Y25','2000-03-10'),(25,'Dhananjoy','PHD','2000-03-15'),(26,'Rakesh Puri','Y24','2000-03-18'),(27,'Ashirwad','Y23','2000-03-19'),(28,'Sujal','Y24','2000-03-19'),(29,'Sumedh','Y21','2000-03-23'),(30,'Yash','Y20','2000-03-25'),(31,'Himanshu Patidar','Y19','2000-03-26'),(32,'Adrishya','Y23','2000-03-27'),(33,'Aradhana Anantha','Y25','2000-04-01'),(34,'Meenakshi Meena','Y25','2000-04-01'),(35,'Padma','Y20','2000-04-02'),(36,'vishal','Y22','2000-04-03'),(37,'shagun chaudhary','Y23','2000-04-03'),(38,'Nirbhay','Y24','2000-04-08'),(39,'Gokul R','Y25','2000-04-13'),(40,'Tanya','Y22','2000-04-13'),(41,'Sameira','Y23','2000-04-19'),(42,'Sneha','Y25','2000-04-23'),(43,'Harsh Mohan','Y21','2000-04-24'),(44,'Jyoti','Y23','2000-04-24'),(45,'Hitesh','Y22','2000-04-26'),(46,'Ram','Y20','2000-05-02'),(47,'Arpita Verma','Y25','2000-05-03'),(48,'Atharv','Y23','2000-05-04'),(49,'Sanjeeta','Y23','2000-05-04'),(50,'Rajender','Y24','2000-05-08'),(51,'Korra Sruthi','Y25','2000-05-11'),(52,'Disha Virmalwar','Y18','2000-05-13'),(53,'Devyani Meena','Y15','2000-05-13'),(54,'Silbina','Y20','2000-05-14'),(55,'Sourabh Sankhala','Y24','2000-05-14'),(56,'Junaid','Y22','2000-05-16'),(57,'Sumanth','Mtech','2000-05-21'),(58,'Nitish','Y24','2000-05-24'),(59,'Lohit','Y21','2000-05-28'),(60,'pushpendra','Y14','2000-06-07'),(61,'Movika','Y23','2000-06-14'),(62,'Harsh Singh','Y22','2000-06-19'),(63,'Maluk','Y23','2000-06-20'),(64,'P Suman','Y24','2000-06-29'),(65,'Kanchan','Y16','2000-07-02'),(66,'Himanshu','Y21','2000-07-02'),(67,'Sandeep','Y20','2000-07-03'),(68,'Shilpee','Y23','2000-07-05'),(69,'Abhijeet','Y17','2000-07-06'),(70,'Tanishq','Y24','2000-07-14'),(71,'Tanish','Y23','2000-07-17'),(72,'Abisanth','Y22','2000-07-21'),(73,'Priyanka','Y22','2000-07-22'),(74,'Manish','Y24','2000-07-22'),(75,'Hemant','Y22','2000-07-30'),(76,'Aditi','Y23','2000-08-01'),(77,'Yogi','Y20','2000-08-05'),(78,'Shruthi','Y19','2000-08-06'),(79,'Ajay neeli chandra','Y17','2000-08-06'),(80,'Dharmendra','Y22','2000-08-10'),(81,'Chandra Bhan','Y23','2000-08-15'),(82,'Anuj','Y23','2000-08-16'),(83,'Ishan','Y23','2000-08-16'),(84,'Manish','Y20','2000-08-19'),(85,'Navjot','Y25','2000-08-19'),(86,'Kuldeep','Y25','2000-08-20'),(87,'Jadav Dathatri','Y24','2000-08-21'),(88,'Bhaskar','Y18','2000-08-29'),(89,'meghna jhakar','Y18','2000-08-29'),(90,'Surya','Y12','2000-09-03'),(91,'Anukalp','Y22','2000-09-14'),(92,'Swarna raj','Y22','2000-09-14'),(93,'Simran','Y20','2000-09-20'),(94,'Ishanvi','Y24','2000-09-21'),(95,'Anshika choudhary','Y18','2000-09-24'),(96,'Vishal','MBA','2000-09-24'),(97,'Sachin nahra','Y18','2000-09-24'),(98,'Saurabh raj','Y24','2000-10-01'),(99,'Karishma','Y24','2000-10-03'),(100,'Antarya','Y22','2000-10-04'),(101,'Sumit','Y22','2000-10-06'),(102,'Mounika S S','Y25','2000-10-08'),(103,'Monika','Y23','2000-10-12'),(104,'Jayesh','Y20','2000-11-01'),(105,'Shreyansh','Y23','2000-11-01'),(106,'Dev Kapil','PHD','2000-11-05'),(107,'Dheeraj','Y22','2000-11-05'),(108,'Anisha','Y23','2000-11-05'),(109,'Nikhil','Y24','2000-11-09'),(110,'R Dheeksha','Y25','2000-11-10'),(111,'Sukhwinder','Y25','2000-11-17'),(112,'Srivanth Guntha','Y25','2000-11-17'),(113,'Pooja','PHD','2000-11-19'),(114,'Abhishek','Y23','2000-11-19'),(115,'Sandhya','Y25','2000-11-29'),(116,'Smira','Y24','2000-11-30'),(117,'Varsha','Y20','2000-12-01'),(118,'Mukul','Y20','2000-12-06'),(119,'Avinash Kumar','Y25','2000-12-06'),(120,'Pooja','Y23','2000-12-10'),(121,'Saurav Raj','Y23','2000-12-11'),(122,'Aman Kumar','Y23','2000-12-13'),(123,'Sanjay Khara','Y23','2000-12-14'),(124,'Ravi Patar','Y24','2000-12-19'),(125,'Devansh','PHD','2000-12-27'),(126,'Adarsh','Y21','2026-01-05'),(127,'demo','y657482','2026-05-19');
/*!40000 ALTER TABLE `birthdays` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int DEFAULT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postponed`
--

DROP TABLE IF EXISTS `postponed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `postponed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Sl` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Sl` (`Sl`),
  CONSTRAINT `postponed_ibfk_1` FOREIGN KEY (`Sl`) REFERENCES `birthdays` (`Sl_no`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postponed`
--

LOCK TABLES `postponed` WRITE;
/*!40000 ALTER TABLE `postponed` DISABLE KEYS */;
/*!40000 ALTER TABLE `postponed` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-18 23:43:57
