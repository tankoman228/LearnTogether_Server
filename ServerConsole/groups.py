import DB


def groups(args):
    db_session = DB.create_session()
    gs = db_session.query(DB.Group).all()
    print("ID_Group\t\tName")
    for g in gs:
        print(f"\t{g.ID_Group}\t\t\t{g.Name}")
    db_session.close()


def create_group(args):
    db_session = DB.create_session()

    gname = ''

    if len(args) == 0:
        args = input('Enter group name')
    else:
        for arg in args:
            gname += arg + ' '

    gname = gname.strip()

    try:
        new_group = DB.Group(Name=gname)
        db_session.add(new_group)
        db_session.commit()

        print('Successfully added. New groups list: ')
        groups(None)
        db_session.close()
    except Exception as e:
        print('database error: ', e)
        db_session.rollback()
        db_session.close()


def delete_group(args):
    db_session = DB.create_session()

    if len(args) == 0:
        args = input('Enter group name')

    gname = ''
    for arg in args:
        gname += arg + ' '
    gname = gname.strip()

    try:
        group = db_session.query(DB.Group).filter(DB.Group.Name == gname).first()
        if not group:
            print('group not found')
            return

        db_session.delete(group)
        db_session.commit()

        print('Successfully deleted. New groups list: ')
        groups(None)
        db_session.close()

    except Exception as e:
        print('database error: ', e)
        db_session.rollback()
        db_session.close()
