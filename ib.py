
class InfoBase:
    def __init__(self, ID_InfoBase=None, ID_Group=None, ID_Account=None, Title=None, Text=None, Tags=None, DateAdd=None):
        self.ID_InfoBase = ID_InfoBase
        self.ID_Group = ID_Group
        self.ID_Account = ID_Account
        self.Title = Title
        self.Text = Text
        self.Tags = Tags
        self.DateAdd = DateAdd

    def save(self):
        if self.ID_InfoBase is None:
            self.insert()
        else:
            self.update()

    def insert(self):
        cnx = mysql.connector.connect(user='username', password='password', host='localhost', database='database')
        cursor = cnx.cursor()

        add_info_base = ("INSERT INTO InfoBase "
                         "(ID_Group, ID_Account, Title, Text, Tags, DateAdd) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")

        data_info_base = (self.ID_Group, self.ID_Account, self.Title, self.Text, self.Tags, self.DateAdd)

        cursor.execute(add_info_base, data_info_base)

        self.ID_InfoBase = cursor.lastrowid

        cnx.commit()

        cursor.close()
        cnx.close()

    def update(self):
        cnx = mysql.connector.connect(user='username', password='password', host='localhost', database='database')
        cursor = cnx.cursor()

        update_info_base = ("UPDATE InfoBase SET "
                            "ID_Group=%s, ID_Account=%s, Title=%s, Text=%s, Tags=%s, DateAdd=%s "
                            "WHERE ID_InfoBase=%s")

        data_info_base = (self.ID_Group, self.ID_Account, self.Title, self.Text, self.Tags, self.DateAdd, self.ID_InfoBase)

        cursor.execute(update_info_base, data_info_base)

        cnx.commit()

        cursor.close()
        cnx.close()

    @staticmethod
    def get_by_id(ID_InfoBase):
        cnx = mysql.connector.connect(user='username', password='password', host='localhost', database='database')
        cursor = cnx.cursor()

        query = ("SELECT ID_InfoBase, ID_Group, ID_Account, Title, Text, Tags, DateAdd "
                 "FROM InfoBase "
                 "WHERE ID_InfoBase = %s")

        cursor.execute(query, (ID_InfoBase,))

        row = cursor.fetchone()

        if row is None:
            return None

        info_base = InfoBase(ID_InfoBase=row[0], ID_Group=row[1], ID_Account=row[2], Title=row[3], Text=row[4], Tags=row[5], DateAdd=row[6])

        cursor.close()
        cnx.close()

        return info_base

