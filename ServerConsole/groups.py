import DB


#  print groups list from database
def groups(args):
    gs = DB.Ses.query(DB.Group).all()
    print("ID_Group\t\tName")
    for g in gs:
        print(f"\t{g.ID_Group}\t\t\t{g.Name}")


def create_group(args):

    gname = ''

    if len(args) == 0:
        args = input('Enter group name')
    else:
        for arg in args:
            gname += arg + ' '

    gname = gname.strip()

    try:
        new_group = DB.Group(Name=gname)
        DB.Ses.add(new_group)
        DB.Ses.commit()

        print('Successfully added. New groups list: ')
        groups(None)
    except Exception as e:
        print('database error: ', e)
        DB.Ses.rollback()


def delete_group(args):
    if len(args) == 0:
        args = input('Enter group name')

    gname = ''
    for arg in args:
        gname += arg + ' '
    gname = gname.strip()

    try:
        group = DB.Ses.query(DB.Group).where(DB.Group.Name == gname).first()
        DB.Ses.delete(group)
        DB.Ses.commit()

        print('Successfully deleted. New groups list: ')
        groups(None)
    except Exception as e:
        print('database error: ', e)
        DB.Ses.rollback()
