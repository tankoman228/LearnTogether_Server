DROP DATABASE IF EXISTS LearnTogether;

CREATE DATABASE LearnTogether CHARACTER SET utf8 COLLATE utf8_general_ci;
USE LearnTogether;

CREATE TABLE `Role`
(
	`ID_Role` INT PRIMARY KEY AUTO_INCREMENT,
	`Name` VARCHAR(128) UNIQUE NOT NULL,
	`IsAdmin` BOOLEAN NOT NULL,
	`AdminLevel` INT DEFAULT 64
);

CREATE TABLE `Permission` 
(
	`ID` 		 INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Role` 	 INT NOT NULL,
	`Name` 		 VARCHAR(64) NOT NULL,
	
	FOREIGN KEY (`ID_Role`) REFERENCES `Role`(`ID_Role`)
	ON DELETE CASCADE
);
CREATE INDEX `p_hash` ON `Permission`(`ID_Role`) USING HASH;
CREATE INDEX `p_sort` ON `Permission`(`ID_Role`);


CREATE TABLE `Group`
(
	`ID_Group` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_BasicRole` INT,
	`Name` VARCHAR(50) UNIQUE NOT NULL,
	`Icon` LONGTEXT,
	`Description` TEXT,
	
	FOREIGN KEY (`ID_BasicRole`) REFERENCES `Role`(`ID_Role`)
	 ON DELETE SET NULL
);

CREATE TABLE `Account`
(
	`ID_Account` INT PRIMARY KEY AUTO_INCREMENT,
	`Username` VARCHAR(70) NOT NULL,
	`Password` TEXT NOT NULL,
	`RecoveryContact` VARCHAR(60),
	`Title` VARCHAR(70) NOT NULL,
	`Icon` LONGTEXT,
	`About` TEXT,
	`Rating` INT DEFAULT 0,
	`LastSeen` DATETIME DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE `Account` ADD UNIQUE INDEX `Username` (`Username`);

CREATE TABLE `AccountGroup`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	`ID_Role` INT,
	
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(`ID_Account`)
	 ON DELETE CASCADE,
	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group)
	ON DELETE CASCADE,
	FOREIGN KEY (ID_Role) REFERENCES `Role`(ID_Role)
	ON DELETE SET NULL
);
CREATE INDEX `AccountGroup_index` ON `AccountGroup`(`ID_Group`);

CREATE TABLE `RegisterToken`
(
	`ID_RegisterToken` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`Text` TEXT NOT NULL,
	`ID_Role` INT,

	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group)
	ON DELETE CASCADE,
	FOREIGN KEY (`ID_Role`) REFERENCES `Role`(ID_Role)
	ON DELETE SET NULL
);
ALTER TABLE `RegisterToken`
	ADD UNIQUE INDEX `Text` (`Text`);
CREATE INDEX `TokenGroup` ON `RegisterToken`(`ID_Group`);

CREATE TABLE `Recovery` (

	`ID_Recovery` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Account` INT NOT NULL,
	`Hash` TEXT,
	`WaitingForGeneration` BOOLEAN NOT NULL,
	
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(`ID_Account`)
	ON DELETE CASCADE
);

CREATE TABLE `Tag` (
	`ID_Tag` INT PRIMARY KEY AUTO_INCREMENT,
	`Text` VARCHAR(32) NOT NULL
);

CREATE TABLE `InfoBase`
(
	`ID_InfoBase` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`ID_Account` INT,
	`Title` VARCHAR(150) NOT NULL,
	`Text` TEXT,
	`Type` CHAR(1), /*n t i m v*/
	`DateAdd` DATE NOT NULL,
	
	FOREIGN KEY (ID_Group) REFERENCES `Group`(ID_Group)
	ON DELETE CASCADE,
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
	ON DELETE SET NULL
);
CREATE INDEX `InfoBase_index` ON `InfoBase`(`ID_Group`);
CREATE INDEX `InfoBase_index2` ON `InfoBase`(`DateAdd`);

CREATE TABLE `InfoTag` (
	`InfoTag` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Tag` INT NOT NULL,
	`ID_InfoBase` INT NOT NULL,
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE,
	FOREIGN KEY (`ID_Tag`) REFERENCES `Tag`(ID_Tag)
	ON DELETE CASCADE
);
CREATE INDEX `info_tag_index` ON `InfoTag`(`ID_Tag`);

CREATE TABLE `ForumAsk`
(
	`ID_ForumAsk` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Solved` BOOLEAN DEFAULT 0,

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `ForumAsk_hash` ON `ForumAsk`(`ID_InfoBase`) USING HASH;

CREATE TABLE `News`
(
	`ID_News` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Images` LONGTEXT,
	Moderated BOOLEAN DEFAULT 0,
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `News_hash` ON `News`(`ID_InfoBase`) USING HASH;

CREATE TABLE `Task`
(
	`ID_Task` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Deadline` DATETIME,
	Moderated BOOLEAN DEFAULT 0,
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `Task_hash` ON `Task`(`ID_InfoBase`) USING HASH;

CREATE TABLE `TaskAccount`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Account` INT NOT NULL,
	`NeedHelp` BOOLEAN NOT NULL,
	`Finished` BOOLEAN NOT NULL,
	`Priority` INT NOT NULL,
	`Progress` INT NOT NULL,

	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
	ON DELETE CASCADE
);
CREATE INDEX `TaskAccount_hash` ON `TaskAccount`(`ID_Account`) USING HASH;

CREATE TABLE `Information`
(
	`ID_Information` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Contents` LONGTEXT,
	`Type` CHAR(1),	/*L - link, I - image, F - file*/

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `Information_hash` ON `Information`(`ID_InfoBase`) USING HASH;

CREATE TABLE `Meeting`
(
	`ID_Meeting` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Starts` DATETIME NOT NULL,
	`Place` VARCHAR(30),
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `Meeting_hash` ON `Meeting`(`ID_InfoBase`) USING HASH;

CREATE TABLE `MeetingRespond`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Meeting` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	`Surety` FLOAT NOT NULL,
	`Start` TIME NOT NULL,
	`End` TIME NOT NULL,
	`Reason` VARCHAR(100),

	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
	ON DELETE CASCADE,
	FOREIGN KEY (`ID_Meeting`) REFERENCES `Meeting`(ID_Meeting)
	ON DELETE CASCADE
);
CREATE INDEX `MRespond_hash_index` ON `MeetingRespond`(`ID_Meeting`);
CREATE INDEX `MRespond_hash` ON `MeetingRespond`(`ID_Account`) USING HASH;

CREATE TABLE `Vote`
(
	`ID_Vote` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Anonymous` BOOLEAN NOT NULL,
	`MultAnswer` BOOLEAN NOT NULL,

	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `Vote_hash` ON `Vote`(`ID_InfoBase`) USING HASH;

CREATE TABLE `VoteItem`
(
	`ID_VoteItem` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Vote` INT NOT NULL,
	`Title`	VARCHAR(20),
	
	FOREIGN KEY (`ID_Vote`) REFERENCES `Vote`(ID_Vote)
	ON DELETE CASCADE
);
CREATE INDEX `Vote` ON `VoteItem`(`ID_Vote`);

CREATE TABLE `VoteAccount`
(
	`ID` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_VoteItem` INT NOT NULL,
	`ID_Account` INT NOT NULL,
	
	FOREIGN KEY (`ID_VoteItem`) REFERENCES `VoteItem`(ID_VoteItem)
	ON DELETE CASCADE,
	FOREIGN KEY (`ID_Account`) REFERENCES `Account`(ID_Account)
	ON DELETE CASCADE
);
CREATE INDEX `VoteAccount_hash` ON `VoteAccount`(`ID_VoteItem`) USING HASH;
CREATE INDEX `VoteAccount_index` ON `VoteAccount`(`ID_Account`);

CREATE TABLE `Comment`
(
	`ID_Comment` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_InfoBase` INT NOT NULL,
	`Rank` INT NOT NULL,
	`Text` TEXT,
	`Attachments` LONGTEXT,
	
	FOREIGN KEY (`ID_InfoBase`) REFERENCES `InfoBase`(ID_InfoBase)
	ON DELETE CASCADE
);
CREATE INDEX `Comment_hash` ON `Comment`(`ID_InfoBase`) USING HASH;

CREATE TABLE `Complaint`
(
	`ID_Complaint` INT PRIMARY KEY AUTO_INCREMENT,
	`ID_Group` INT NOT NULL,
	`Sender` INT NOT NULL,
	`Suspected` INT NOT NULL,
	`Reason` VARCHAR(400),
	`DateTime` DATETIME,
	Moderated BOOLEAN DEFAULT 0,
	
	FOREIGN KEY (`ID_Group`) REFERENCES `Group`(ID_Group)
	ON DELETE CASCADE,
	FOREIGN KEY (`Sender`) REFERENCES `Account`(ID_Account)
	ON DELETE CASCADE,
	FOREIGN KEY (`Suspected`) REFERENCES `Account`(ID_Account)
	ON DELETE CASCADE
);