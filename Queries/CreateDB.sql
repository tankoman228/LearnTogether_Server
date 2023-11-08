DROP DATABASE IF EXISTS LearnTogether;

CREATE DATABASE LearnTogether CHARACTER SET utf8 COLLATE utf8_general_ci;
USE LearnTogether;

CREATE TABLE `Group`
(
	`ID_Group` INT PRIMARY KEY AUTO_INCREMENT,
	`Name` VARCHAR(50) UNIQUE NOT NULL,
	`Icon` LONGTEXT,
	`Description` TEXT
);

CREATE TABLE `Account`
(
	`ID_Account` INT PRIMARY KEY AUTO_INCREMENT,
	`Username` VARCHAR(70) NOT NULL,
	`Password` TEXT,
	`RecoveryContact` VARCHAR(60),
	`Title` VARCHAR(70) NOT NULL,
	`Icon` LONGTEXT,
	`About` TEXT,
	`IsAdmin` BOOLEAN NOT NULL,
	`AdminLevel` TINYINT DEFAULT 0,
	`Rating` INT DEFAULT 0,
	`LastSeen` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `AccountGroup`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(`ID_Account`),
	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group)
);

CREATE TABLE `Limitation` 
(
	`ID` 		 INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Account` INT NOT NULL,
	`List` 		 LONGTEXT NOT NULL,
	`AdminLevel` TINYINT NOT NULL,
	
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(`ID_Account`)
);

CREATE TABLE `RegisterToken`
(
	`ID_RegisterToken` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`Hash` TEXT NOT NULL,
	`Enabled` BOOLEAN NOT NULL,
	`Admin` BOOLEAN NOT NULL,
	`AdminLevel` TINYINT NOT NULL,

	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group)
);

CREATE TABLE `Recovery` (

	`ID_Recovery` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Account` INT NOT NULL,
	`Hash` TEXT,
	`WaitingForGeneration` BOOLEAN NOT NULL,
	
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(`ID_Account`)
);

CREATE TABLE `Tag` (
	`ID_Tag` INT PRIMARY KEY AUTO_INCREMENT,
	`Text` VARCHAR(32) NOT NULL
);

CREATE TABLE `InfoBase`
(
	`ID_InfoBase` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	`Title` VARCHAR(150) NOT NULL,
	`Text` TEXT,
	`DateAdd` DATE NOT NULL,
	
	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group),
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
);

CREATE TABLE `InfoTag` (
	`InfoTag` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Tag` INT NOT NULL,
	`ID_InfoBase` INT NOT NULL,
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase),
	FOREIGN KEY (`ID_Tag`) REFERENCES `Tag`(ID_Tag)
);

CREATE TABLE `ForumAsk`
(
	`ID_ForumAsk` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Solved` BOOLEAN DEFAULT 0,

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `News`
(
	`ID_News` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Images` LONGTEXT,
	Moderated BOOLEAN DEFAULT 0,
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `Task`
(
	`ID_Task` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Deadline` DATETIME,
	Moderated BOOLEAN DEFAULT 0,
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `TaskAccount`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Account` INT NOT NULL,
	`NeedHelp` BOOLEAN NOT NULL,
	`Finished` BOOLEAN NOT NULL,
	`Priority` TINYINT NOT NULL,
	`Progress` TINYINT NOT NULL,

	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
);

CREATE TABLE `Information`
(
	`ID_Information` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Contents` LONGTEXT,
	`Type` CHAR(1),	/*L - link, I - image, F - file*/

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `Meeting`
(
	`ID_Meeting` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Starts` DATETIME NOT NULL,
	`Place` VARCHAR(30),
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `MeetingRespond`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Meeting` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	`Surety` FLOAT NOT NULL,
	`Start` TIME NOT NULL,
	`End` TIME NOT NULL,
	`Reason` VARCHAR(100),

	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account),
	FOREIGN KEY (`ID_Meeting`) REFERENCES `Meeting`(ID_Meeting)
);

CREATE TABLE `Vote`
(
	`ID_Vote` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Anonymous` BOOLEAN NOT NULL,
	`MultAnswer` BOOLEAN NOT NULL,

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `VoteItem`
(
	`ID_VoteItem` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Vote` INT NOT NULL,
	`Title`	VARCHAR(20),
	
	FOREIGN KEY (`ID_Vote`) REFERENCES `Vote`(ID_Vote)
);

CREATE TABLE `VoteAccount`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_VoteItem` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	
	FOREIGN KEY (`ID_VoteItem`) REFERENCES `VoteItem`(ID_VoteItem),
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
);

CREATE TABLE `Comment`
(
	`ID_Comment` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Rank` TINYINT NOT NULL,
	`Text` TEXT,
	`Attachments` LONGTEXT,
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
);

CREATE TABLE `Complaint`
(
	`ID_Complaint` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`Sender` INT NOT NULL,
	`Suspected` INT NOT NULL,
	`Reason` VARCHAR(400),
	`DateTime` DATETIME,
	Moderated BOOLEAN DEFAULT 0,
	
	FOREIGN KEY (`ID_Group`) REFERENCES `Group`(ID_Group),
	FOREIGN KEY (`Sender`) REFERENCES `Account`(ID_Account),
	FOREIGN KEY (`Suspected`) REFERENCES `Account`(ID_Account)
);