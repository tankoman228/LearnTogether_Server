import os
import re

input_str = "'NeedHelp', 'AccountTitle', 'Author', 'About', 'Rating', 'Role', 'Start', 'Sender', 'Username', 'ID_Vote', 'ID_Role', 'Account', 'PeopleJoined', 'Items', 'WhenAdd', 'LastSeen', 'StartsAt', 'ID_InfoBase', 'Finished', 'ID_Task', 'Reason', 'ID_News', 'Item', 'Text', 'Deadline', 'TaskTitle', 'Surety', 'Type', 'Progress', 'IsAdmin', 'Permissions', 'Anonymous', 'Title', 'Moderated', 'ID_Complaint', 'Suspected', 'Rate', 'Priority', 'SuspectedID', 'End', 'Name', 'ID_Meeting', 'Images', 'CommentsFound', 'Count', 'ID_Comment', 'Place', 'ID_Author', 'Avatar', 'ID_Account', 'AuthorTitle', 'Attachment', 'ID_Information', 'SenderID', 'DateTime', 'Icon', 'AdminLevel', 'ID_ForumAsk', 'Solved'"

variable_names = [name.strip().strip("'") for name in input_str.split(',')]

# Генерируем Java класс
java_class = "import com.google.gson.annotations.SerializedName;\n\n"
java_class += "public class GeneratedClass {\n\n"

for name in variable_names:
    var_type = "String" if "ID" not in name else "int"
    java_class += f"\t@SerializedName(\"{name}\")\n"
    java_class += f"\tpublic {var_type} {name};\n\n"

java_class += "}"

print(java_class)