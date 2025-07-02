/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - skillswapping
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`skillswapping` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `skillswapping`;

/*Table structure for table `badgeorchive` */

DROP TABLE IF EXISTS `badgeorchive`;

CREATE TABLE `badgeorchive` (
  `badgeorchive_id` int(11) NOT NULL AUTO_INCREMENT,
  `badgeorchive` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`badgeorchive_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `badgeorchive` */

insert  into `badgeorchive`(`badgeorchive_id`,`badgeorchive`) values 
(1,'badge1'),
(2,'achive1'),
(3,'badge2'),
(4,'achive2');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `category` */

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`sender_id`,`receiver_id`,`message`,`date`) values 
(1,2,2,'hi','2024-01-04');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

/*Table structure for table `highlights` */

DROP TABLE IF EXISTS `highlights`;

CREATE TABLE `highlights` (
  `highlight_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `highlights` varchar(100) DEFAULT NULL,
  `image` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`highlight_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `highlights` */

insert  into `highlights`(`highlight_id`,`project_id`,`highlights`,`image`) values 
(1,1,'gghjd','static/images/79187db0-a211-4383-b8a1-d22869df62171704368169496.png'),
(2,1,'dgghh','static/images/888eb801-099b-488e-b355-d02356857d0f1704368360043.png');

/*Table structure for table `issues` */

DROP TABLE IF EXISTS `issues`;

CREATE TABLE `issues` (
  `issues_id` int(11) NOT NULL AUTO_INCREMENT,
  `prequest_id` int(11) DEFAULT NULL,
  `issues` varchar(100) DEFAULT NULL,
  `images` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`issues_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `issues` */

insert  into `issues`(`issues_id`,`prequest_id`,`issues`,`images`) values 
(1,1,'rjdjxk','static/images/4f92071d-a611-48a4-8f9d-a6b28d9149f01704369798723.png');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'anu','12345','user'),
(2,'maya','12344','user');

/*Table structure for table `myskills` */

DROP TABLE IF EXISTS `myskills`;

CREATE TABLE `myskills` (
  `myskills_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `badgeorchive_id` int(11) DEFAULT NULL,
  `skills_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`myskills_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `myskills` */

insert  into `myskills`(`myskills_id`,`user_id`,`badgeorchive_id`,`skills_id`) values 
(1,1,1,1),
(2,2,3,3);

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `request_id` int(11) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`request_id`,`type`,`amount`,`date`) values 
(1,1,'skill','400','2024-01-04');

/*Table structure for table `prequest` */

DROP TABLE IF EXISTS `prequest`;

CREATE TABLE `prequest` (
  `prequest_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`prequest_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `prequest` */

insert  into `prequest`(`prequest_id`,`user_id`,`project_id`,`date`,`status`) values 
(1,2,1,'2024-01-04','accept');

/*Table structure for table `projects` */

DROP TABLE IF EXISTS `projects`;

CREATE TABLE `projects` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `projects` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `projects` */

insert  into `projects`(`project_id`,`user_id`,`projects`,`details`,`date`,`amount`,`status`) values 
(1,1,'pro1','gdjdnnx','2024-01-04','2000','Available');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `myskills_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `request` */

insert  into `request`(`request_id`,`myskills_id`,`user_id`,`amount`,`details`,`date`,`status`) values 
(1,2,1,'400','hfjfjf','2024-01-04','paid'),
(2,1,1,'pending','uuu','2024-01-04','pending');

/*Table structure for table `skills` */

DROP TABLE IF EXISTS `skills`;

CREATE TABLE `skills` (
  `skills_id` int(11) NOT NULL AUTO_INCREMENT,
  `skills` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`skills_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `skills` */

insert  into `skills`(`skills_id`,`skills`) values 
(1,'php'),
(2,'html'),
(3,'python');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `ufname` varchar(100) DEFAULT NULL,
  `ulname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`ufname`,`ulname`,`place`,`phone`,`email`) values 
(1,1,'anu','k','ernakulam','7561074531','a@gmail.com'),
(2,2,'maya','y','south','7593938854','s@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
