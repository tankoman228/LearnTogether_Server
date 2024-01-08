INSERT INTO `Role` (`ID_Role`, `Name`, `IsAdmin`, `AdminLevel`) VALUES ('1', 'Student', '0', '0');
INSERT INTO `Role` (`ID_Role`, `Name`, `IsAdmin`) VALUES ('2', 'Admin', '1');
INSERT INTO `Role` (`ID_Role`, `Name`, `IsAdmin`, `AdminLevel`) VALUES ('3', 'Owner', '1', '127');


INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (1, 'offer_publications');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (1, 'forum_allowed');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (1, 'comments_allowed');

INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'moderate_publications');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'offer_publications');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'edit_roles');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'forum_allowed');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'comments_allowed');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'moderate_comments');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (2, 'ban_accounts');

INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'moderate_publications');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'offer_publications');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'edit_roles');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'edit_group');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'forum_allowed');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'comments_allowed');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'moderate_comments');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'create_tokens');
INSERT INTO `Permission` (`ID_Role`, `Name`) VALUES (3, 'ban_accounts');