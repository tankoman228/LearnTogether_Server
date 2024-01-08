from sqlalchemy import text

import DB


def roles_out(args):
    rs = DB.Ses.query(DB.Role).all()
    for r in rs:
        print(f"ID: {r.ID_Role}\t Name: {r.Name} \n\tPermissions:")
        ps = DB.Ses.query(DB.Permission).where(DB.Permission.ID_Role == int(r.ID_Role))
        for p in ps:
            print(f"\t\t{p.Name}")
        print()
    print('FIRST 3 ARE CONSTANTS')


def create_role(args):
    if len(args) < 2:
        print('Not enough args. Cannot execute your command')
        return

    try:
        base_permissions = DB.Ses.query(DB.Permission).where(DB.Permission.ID_Role == int(args[1])).all()
        if len(base_permissions) <= 0:
            raise Exception('no permissions for such role id')

        new_role = DB.Role(Name=args[0], IsAdmin=((args[1] != 1) and (int(args[1]) < 4)))
        DB.Ses.add(new_role)
        DB.Ses.commit()

        for base_permission in base_permissions:
            permission = DB.Permission(ID_Role=new_role.ID_Role, Name=base_permission.Name)
            DB.Ses.add(permission)
        DB.Ses.commit()

        print('Success! New role has permissions: ')
        for base_permission in base_permissions:
            print('\t', base_permission.Name)

    except Exception as e:
        print('Cannot create role cause: ', e)


def delete_role(args):
    if len(args) == 0:
        args = input('Enter group name')

    if int(args[0]) <= 3:
        print('Can\'t delete basic role')
        return

    try:
        role = DB.Ses.query(DB.Role).where(DB.Role.ID_Role == int(args[0])).first()
        DB.Ses.delete(role)
        DB.Ses.commit()

        print('Successfully deleted. New roles list: ')
        roles_out(None)
    except Exception as e:
        print('database error: ', e)
        DB.Ses.rollback()


def change_permissions(args):

    if len(args) < 1:
        print('no role id selected')
        return

    if int(args[0]) == 3:
        print('Can\'t edit this role')
        return

    current_permissions = DB.Ses.query(DB.Permission).where(DB.Permission.ID_Role == int(args[0])).all()
    current_permissions_names = []

    if len(current_permissions) < 1:
        if input('No permissions for this role found. Print 1 if you are sure the id is right') != '1':
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
            i = 0
            for av_perm in available_to_add_permissions:
                print(f'\t {i} : {av_perm}')
                i += 1

            i = int(input('\n'))
            if i >= len(available_to_add_permissions):
                print('No such number in list')
                continue

            try:
                new_perm_name = available_to_add_permissions[i]
                permission = DB.Permission(ID_Role=int(args[0]), Name=new_perm_name)
                DB.Ses.add(permission)
                DB.Ses.commit()

                available_to_add_permissions.pop(i)

                print('Success!')
            except Exception as e:
                print('Unknown error: ', e)
                DB.Ses.rollback()

        elif input('print 1 to delete permission ') == '1':

            print(' Permissions for this role are: ')
            for base_permission in current_permissions:
                print('\t', base_permission.Name)
                current_permissions_names.append(base_permission.Name)

            try:
                name = input('\nprint permission\'s name to delete ')

                if name in all_permissions_names:
                    DB.Ses.execute(text('DELETE FROM `Permission` WHERE `ID_Role` = \'' + args[0] + '\''
                                        + ' AND `Name` = \'' +
                                        name + '\''))
                    DB.Ses.commit()

                    available_to_add_permissions.append(name)
                    print('Success')
                else:
                    print('this permission does not exist')

            except Exception as e:
                print('Error: ', e)
                DB.Ses.rollback()

    print(' editing permissions finished')
