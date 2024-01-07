import DB


def roles_out(args):
    rs = DB.SessionEngine.query(DB.Role).all()
    for r in rs:
        print(f"ID: {r.ID_Role}\t Name: {r.Name} \n\tPermissions:")
        ps = DB.SessionEngine.query(DB.Permission).where(DB.Permission.ID_Role == int(r.ID_Role))
        for p in ps:
            print(f"\t\t{p.Name}")
        print()
    print('FIRST 3 ARE CONSTANTS')


def create_role(args):
    if len(args) < 2:
        print('Not enough args. Cannot execute your command')
        return

    try:
        base_permissions = DB.SessionEngine.query(DB.Permission).where(DB.Permission.ID_Role == int(args[1])).all()
        if len(base_permissions) <= 0:
            raise Exception('no permissions for such role id')

        new_role = DB.Role(Name=args[0], IsAdmin=((args[1] != 1) & (int(args[1]) < 4)))
        DB.SessionEngine.add(new_role)
        DB.SessionEngine.commit()

        for base_permission in base_permissions:
            permission = DB.Permission(ID_Role=new_role.ID_Role, Name=base_permission.Name)
            DB.SessionEngine.add(permission)
        DB.SessionEngine.commit()

        print('Success! New role has permissions: ')
        for base_permission in base_permissions:
            print('\t', base_permission.Name)

    except Exception as e:
        print('Cannot create role cause: ', e)


def delete_role(args):
    pass


def change_permissions(args):
    pass
