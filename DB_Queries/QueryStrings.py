insert_token = '''
INSERT INTO `RegisterToken` (`ID_Group`, `Text`, `Admin`, `AdminLevel`)
VALUES (%s, %s, %s, %s)'''

delete_token = '''
DELETE FROM `RegisterToken` WHERE `Text` = %s
'''

insert_group = '''
INSERT INTO `Group` (`Name`, `Description`) VALUES (%s, %s)
'''

update_group = '''
UPDATE `Group` SET `Name` = %s, `Description` = %s WHERE `ID_Group` = %s
'''

update_group_icon = '''
UPDATE `Group` SET `Icon` = %s 
'''

delete_group = '''
DELETE FROM `Group` WHERE `ID_Group` = %s
'''