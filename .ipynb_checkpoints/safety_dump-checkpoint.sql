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
INSERT INTO `admins` VALUES ('1234','pbkdf2:sha256:50000$pPGHnD8y$afe425b0f716a6c5a84cbed31a645c6fe8f61dfde1775a9cc3a34c92ab9a7c44'),('admin','pbkdf2:sha256:50000$SBkHcINZ$b75c69ba6594761c955e9928b2ef5f83c56fee70b5e872bdfc416e9cedbd69bf');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favourites`
--

DROP TABLE IF EXISTS `favourites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favourites` (
  `username` varchar(20) NOT NULL,
  `video_ID` varchar(50) NOT NULL,
  PRIMARY KEY (`username`,`video_ID`),
  KEY `video_ID` (`video_ID`),
  CONSTRAINT `favourites_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE,
  CONSTRAINT `favourites_ibfk_2` FOREIGN KEY (`video_ID`) REFERENCES `videos` (`video_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favourites`
--

LOCK TABLES `favourites` WRITE;
/*!40000 ALTER TABLE `favourites` DISABLE KEYS */;
INSERT INTO `favourites` VALUES ('mohandas','MjAyMDQ0OTk1MDIzMTU4'),('sharad','MjAyMDQ0OTk1MDIzMTU4'),('sharad','MTgxNjg0MDQzODA4NjM5');
/*!40000 ALTER TABLE `favourites` ENABLE KEYS */;
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
INSERT INTO `flags` VALUES ('MTM3ODkyMjcwODAzOTIw','mohandas');
/*!40000 ALTER TABLE `flags` ENABLE KEYS */;
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
INSERT INTO `users` VALUES ('daftpunk','pbkdf2:sha256:50000$avlzcrje$3d6e0dba154af8b9a0abc45de93cabb450c5834cb8de5deb321cec685c4a91ff'),('deadmau5','pbkdf2:sha256:50000$bCaes6UZ$fa4c922ed30fdeacb5938318cbe2bc68b88577ba6510f76456225c438d2b537c'),('dondiablo','pbkdf2:sha256:50000$zGwOuXxr$13cf193070a1517592c0cf8dd3089a25aa05e3ff25ee76ae2e0746257313df3b'),('joji','pbkdf2:sha256:50000$WAIDcc8m$ac6e60e1a215a740cf9b3515ad6a3950cf06da5a6da4e0a65da960de63be351b'),('jonbellion','pbkdf2:sha256:50000$2fZRgdLi$491b0b44fcf4cd2a36de6d71fad7ab909915afaad6445e697fc680cdc58376c6'),('kshmr','pbkdf2:sha256:50000$1XdqpFZz$3ca79b5840f95b361b0ec09c06ac5298fc5a1fcccf039b3648e67e1e3f10739d'),('mohandas','pbkdf2:sha256:50000$ojhpnoe3$f75644e6becbe539f875070f3e4e2679b32809fa4df73088aeb80d8c2238ec50'),('pawan','pbkdf2:sha256:50000$9nlEZryw$52597d17fd3f0e1724c305b1c3837813d22609202b262cd0a82c057aeca9b1cc'),('sharad','pbkdf2:sha256:50000$dBSIUB36$8abbfa3e928ac0a27ec4bafdac11e6670a612dbb19da2570ab6e8379faa72483'),('skrillex','pbkdf2:sha256:50000$CE4rJ9GQ$e7182f450eb1403846a738bc923ce7dac16ee8fb3121a0c3279225fb99e767b1'),('suman','pbkdf2:sha256:50000$dKyaAVrA$58c57844ff4e20fc52aae9d9f1eb25dc4360721c0352b1999afbb6a40312e12f'),('trapcity','pbkdf2:sha256:50000$ZloYB9X8$41e4e1b279d16939a5b9019145e8cbd3d1c810f974d751c30b6676a499d011f8');
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
  `upload_date` date DEFAULT NULL,
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
INSERT INTO `videos` VALUES ('MjA5MTQxMjQwMzQ2Njc0','Skrillex - Bangarang feat. Sirah','skrillex','1','2017-11-05'),('MjAyMDQ0OTk1MDIzMTU4','Flume & Chet Faker - Drop the Game','mohandas','22','2017-11-05'),('MjAyODE2OTQyMzczMTg2','Getter - Rip N Dip (Official Music Video)','mohandas','2','2017-11-23'),('MjczODc2MDA2Nzc2MTM=','The Weeknd - I Feel It Coming ft. Daft Punk','daftpunk','1','2017-11-05'),('MjEyMzQyMjYyOTk4ODUz','KSHMR - Jammu','kshmr','3','2017-11-05'),('MjEzNDg2MTM2NDU0NTI3','Daft Punk - Instant Crush ft. Julian Casablancas','daftpunk','3','2017-11-05'),('MjQzMDkyOTAyMzIxMTk1','deadmau5 feat. Rob Swire - Ghosts N Stuff','deadmau5','1','2017-11-05'),('MjYyMDc4ODk5MDkwNjg3','Kendrick Lamar - Humble (Skrillex Remix)','skrillex','1','2017-11-05'),('MTcwMTkzNDQ0MzAwMDA1','KSHMR & Marnik - Bazaar','kshmr','2','2017-11-03'),('MTgxNjg0MDQzODA4NjM5','Galantis - Hey Alligator (T-Mass Remix)','trapcity','14','2017-11-06'),('MTgyOTcxODM1MDQ2OTAw','Don Diablo - Drifter ft. DYU','dondiablo','1','2017-11-03'),('MTIxMTg4ODIxNjU0MDEw','Bastille - Good Grief (Don Diablo Remix)','dondiablo','1','2017-11-03'),('MTkxMzQwNTgyODQ5OTg3','Zonderling - Tunnel Vision (Don Diablo Edit)','dondiablo','1','2017-11-03'),('MTM3ODkyMjcwODAzOTIw','Justin Prime & Onderkoffer feat. Taylor Jones - Lights Off','trapcity','7','2017-11-06'),('NDE5MzkwOTc4MzM1NDU=','KSHMR & MARNIK - Mandala ft. Mitika','kshmr','1','2017-11-01'),('NTE3MzAzODk0NzMxNDI=','Daft Punk - Get Lucky','daftpunk','1','2017-11-02'),('NTI2NjY5OTk1MjI2NTc=','Jon Bellion - All Time Low','jonbellion','5','2017-11-07'),('NTYwNDcwNzI5NjYwODA=','deadmau5 - Let Go Feat. Grabbitz','deadmau5','4','2017-11-08'),('NzE5OTI5NzY5ODM5NDE=','Joji - I Don\'t Wanna Waste My Time','joji','1','2017-11-01'),('ODc4Mjg2MTYyMDk4NDU=','Skrillex & Poo Bear - Would You Ever','skrillex','4','2017-11-04'),('ODkxODIyOTMyMDQwODQ=','Pawan\'s v','pawan','3','2017-11-10'),('ODYyOTgwNTA2NjQwMDA=','Joji - Will He','joji','1','2017-11-04'),('OTg3MTMzODkzMTYyNzQ=','deadmau5 x Shotty Horroh - Legendary','deadmau5','2','2017-11-04');
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER add_date BEFORE INSERT ON `videos`
FOR EACH ROW
BEGIN
SET NEW.upload_date = DATE(NOW());
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `watched`
--

DROP TABLE IF EXISTS `watched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `watched` (
  `video_ID` varchar(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  `count` varchar(10) DEFAULT NULL,
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
INSERT INTO `watched` VALUES ('MjA5MTQxMjQwMzQ2Njc0','skrillex','1'),('MjAyMDQ0OTk1MDIzMTU4','mohandas','5'),('MjAyMDQ0OTk1MDIzMTU4','sharad','14'),('MjAyODE2OTQyMzczMTg2','mohandas','2'),('MjczODc2MDA2Nzc2MTM=','daftpunk','1'),('MjEyMzQyMjYyOTk4ODUz','kshmr','1'),('MjEyMzQyMjYyOTk4ODUz','pawan','1'),('MjEyMzQyMjYyOTk4ODUz','sharad','1'),('MjEzNDg2MTM2NDU0NTI3','daftpunk','1'),('MjEzNDg2MTM2NDU0NTI3','pawan','2'),('MjQzMDkyOTAyMzIxMTk1','deadmau5','1'),('MjYyMDc4ODk5MDkwNjg3','skrillex','1'),('MTcwMTkzNDQ0MzAwMDA1','kshmr','1'),('MTcwMTkzNDQ0MzAwMDA1','sharad','1'),('MTgxNjg0MDQzODA4NjM5','sharad','5'),('MTgxNjg0MDQzODA4NjM5','trapcity','3'),('MTgyOTcxODM1MDQ2OTAw','dondiablo','1'),('MTIxMTg4ODIxNjU0MDEw','dondiablo','1'),('MTkxMzQwNTgyODQ5OTg3','dondiablo','1'),('MTM3ODkyMjcwODAzOTIw','mohandas','2'),('MTM3ODkyMjcwODAzOTIw','sharad','1'),('MTM3ODkyMjcwODAzOTIw','trapcity','1'),('NDE5MzkwOTc4MzM1NDU=','kshmr','1'),('NTE3MzAzODk0NzMxNDI=','daftpunk','1'),('NTI2NjY5OTk1MjI2NTc=','jonbellion','1'),('NTI2NjY5OTk1MjI2NTc=','pawan','3'),('NTYwNDcwNzI5NjYwODA=','deadmau5','1'),('NTYwNDcwNzI5NjYwODA=','sharad','2'),('NzE5OTI5NzY5ODM5NDE=','joji','1'),('ODc4Mjg2MTYyMDk4NDU=','sharad','3'),('ODc4Mjg2MTYyMDk4NDU=','skrillex','1'),('ODkxODIyOTMyMDQwODQ=','pawan','3'),('ODYyOTgwNTA2NjQwMDA=','joji','1'),('OTg3MTMzODkzMTYyNzQ=','deadmau5','1'),('OTg3MTMzODkzMTYyNzQ=','sharad','1');
/*!40000 ALTER TABLE `watched` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'video'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_to_fav` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_to_fav`(IN ID VARCHAR(50), IN watcher VARCHAR(20))
BEGIN
DECLARE count1 VARCHAR(10);
DECLARE cur1 CURSOR FOR (SELECT count FROM watched WHERE video_ID = ID AND username = watcher AND NOT EXISTS (SELECT * FROM favourites WHERE username = watcher AND video_ID = ID));
OPEN cur1;
FETCH cur1 INTO count1;
IF count1 >= 5 THEN
INSERT INTO favourites VALUES(watcher, ID);
END IF;
CLOSE cur1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-23  3:07:17
