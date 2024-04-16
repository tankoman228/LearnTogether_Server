from sqlalchemy import text

import DB


def roles_out(args):
    db_session = DB.create_session()
    rs = db_session.query(DB.Role).all()
    for r in rs:
        print(f"ID: {r.ID_Role}\t Name: {r.Name} \n\tPermissions:")
        ps = r.permissions
        for p in ps:
            print(f"\t\t{p.Name}")
        print()
    db_session.close()


def create_role(args):
    db_session = DB.create_session()
    if len(args) < 2:
        print('Not enough args. Cannot execute your command')
        db_session.close()
        return

    try:
        base_permissions = db_session.query(DB.Role).filter(DB.Role.ID_Role == int(args[1])).first().permissions
        if not base_permissions or len(base_permissions) <= 0:
            raise Exception('no permissions for such role id')

        new_role = DB.Role(Name=args[0], IsAdmin=((args[1] != 1) and (int(args[1]) < 4)))
        db_session.add(new_role)
        db_session.commit()

        for base_permission in base_permissions:
            permission = DB.Permission(ID_Role=new_role.ID_Role, Name=base_permission.Name)
            db_session.add(permission)
        db_session.commit()

        print('Success! New role has permissions: ')
        for base_permission in base_permissions:
            print('\t', base_permission.Name)

    except Exception as e:
        print('Cannot create role cause: ', e)
    finally:
        db_session.close()


def delete_role(args):
    db_session = DB.create_session()
    if len(args) == 0:
        args = input('Enter group name')

    if int(args[0]) <= 3:
        print('Can\'t delete basic role')
        db_session.close()
        return

    try:
        role = db_session.query(DB.Role).filter(DB.Role.ID_Role == int(args[0])).first()
        db_session.delete(role)
        db_session.commit()

        print('Successfully deleted. New roles list: ')
        roles_out(None)
    except Exception as e:
        print('database error: ', e)
        db_session.rollback()
    finally:
        db_session.close()


def change_permissions(args):
    db_session = DB.create_session()
    if len(args) < 1:
        print('no role id selected')
        db_session.close()
        return

    if int(args[0]) == 3:
        print('Can\'t edit this role')
        db_session.close()
        return

    current_permissions = db_session.query(DB.Permission).filter(DB.Permission.ID_Role == int(args[0])).all()
    current_permissions_names = []

    if len(current_permissions) < 1:
        if input('No permissions for this role found. Print 1 if you are sure the id is right') != '1':
            db_session.close()
            return

    print(' Permissions for this role are: ')
    for base_permission in current_permissions:
        print('\t', base_permission.Name)
        current_permissions_names.append(base_permission.Name)

    all_permissions_names = [
        'moderate_publications',
        'offer_publications',
        'edit_roles',
        'edit_group' ,
        'forum_allowed',
        'comments_allowed',
        'moderate_comments',
        'create_tokens',
        'ban_accounts']
    available_to_add_permissions = []

    for permissions_name in all_permissions_names:
        if permissions_name not in current_permissions_names:
            available_to_add_permissions.append(permissions_name)

    while input('print 1 to continue editing ') == '1':

        if input('print 1 to add new permission ') == '1' and len(current_permissions) < len(all_permissions_names):

            print('\n Select permission to add (print number)')
            i = int(input('\n'))
            for av_perm in available_to_add_permissions:
                print(f'\t {i} : {av_perm}')
                i += 1

    db_session.close()