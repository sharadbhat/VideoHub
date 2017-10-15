-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: localhost    Database: video
-- ------------------------------------------------------
-- Server version	5.7.19-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `video`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `video` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `video`;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admins` (
  `username` varchar(20) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('admin','pbkdf2:sha256:50000$SBkHcINZ$b75c69ba6594761c955e9928b2ef5f83c56fee70b5e872bdfc416e9cedbd69bf');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flags`
--

DROP TABLE IF EXISTS `flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flags` (
  `video_ID` varchar(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  PRIMARY KEY (`video_ID`,`username`),
  KEY `username` (`username`),
  CONSTRAINT `flags_ibfk_1` FOREIGN KEY (`video_ID`) REFERENCES `videos` (`video_ID`) ON DELETE CASCADE,
  CONSTRAINT `flags_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flags`
--

LOCK TABLES `flags` WRITE;
/*!40000 ALTER TABLE `flags` DISABLE KEYS */;
/*!40000 ALTER TABLE `flags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ratings` (
  `video_ID` varchar(50) NOT NULL,
  `rater_username` varchar(20) NOT NULL,
  PRIMARY KEY (`video_ID`,`rater_username`),
  KEY `rater_username` (`rater_username`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`video_ID`) REFERENCES `videos` (`video_ID`) ON DELETE CASCADE,
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`rater_username`) REFERENCES `users` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('shaman','pbkdf2:sha256:50000$H6a2hucn$64c62fe57274b8266f9cc92e27b35fb672c6b287534a0f963fa0151b4383b228'),('sharad','pbkdf2:sha256:50000$zZ9aZwUa$6a4cddef7242dd77421edbd618e08354723e4804a7a065b803f1ade437e298e7');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `videos` (
  `video_ID` varchar(50) NOT NULL,
  `video_title` varchar(200) DEFAULT NULL,
  `uploader` varchar(20) DEFAULT NULL,
  `view_count` varchar(10) DEFAULT NULL,
  `upvotes` varchar(10) DEFAULT NULL,
  `downvotes` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`video_ID`),
  KEY `uploader` (`uploader`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`uploader`) REFERENCES `users` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES ('MjI2MjE2OTAxNjUzMTAy','Joji - I Don\'t Wanna Waste My Time','sharad','3','0','0'),('MTc3MTcxNTY2MjM4MTgx','Zonderling - Tunnel Vision (Don Diablo Edit)','sharad','7','0','0'),('MTg2NTA1MTgxODQwNTEw','Skrillex - Bangarang feat. Sirah','sharad','3','0','0'),('MTM1MDAzMDE2Mjg2NzA2','Don Diablo - Drifter ft. DYU','sharad','1','0','0'),('MTU2MDY1NzMzMjI0Nzg2','KSHMR - Jammu','sharad','1','0','0');
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watched`
--

DROP TABLE IF EXISTS `watched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `watched` (
  `video_ID` varchar(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  PRIMARY KEY (`video_ID`,`username`),
  KEY `username` (`username`),
  CONSTRAINT `watched_ibfk_1` FOREIGN KEY (`video_ID`) REFERENCES `videos` (`video_ID`) ON DELETE CASCADE,
  CONSTRAINT `watched_ibfk_2` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watched`
--

LOCK TABLES `watched` WRITE;
/*!40000 ALTER TABLE `watched` DISABLE KEYS */;
INSERT INTO `watched` VALUES ('MjI2MjE2OTAxNjUzMTAy','shaman'),('MjI2MjE2OTAxNjUzMTAy','sharad'),('MTc3MTcxNTY2MjM4MTgx','sharad'),('MTg2NTA1MTgxODQwNTEw','sharad'),('MTM1MDAzMDE2Mjg2NzA2','sharad'),('MTU2MDY1NzMzMjI0Nzg2','sharad');
/*!40000 ALTER TABLE `watched` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-16  1:53:15
