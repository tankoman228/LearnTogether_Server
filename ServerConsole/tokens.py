from sqlalchemy import text

import DB


def tokens(args):
    db_session = DB.create_session()
    print('ATTENTION! Tokens must be hidden from other users. Don\'t give screenshot to everyone and '
          'give token for one user only \n')

    print('Tokens list:')
    ts = db_session.query(DB.RegisterToken).all()

    if len(ts) == 0:
        print('<empty>')

    for t in ts:
        print(f'ID: {t.ID_RegisterToken} \t| Group[{t.group.ID_Group}]: {t.group.Name} '
              f'\t| Role[{t.role.ID_Role}]: {t.role.Name} \t |  {t.Text}  |')

    db_session.close()


def create_token(args):
    db_session = DB.create_session()
    if len(args) != 3:
        print('Wrong args number. Right args are: <id_group> <id_role> <token_string>')
        db_session.close()
        return

    try:
        new_token = DB.RegisterToken(ID_Group=int(args[0]), ID_Role=int(args[1]), Text=args[2])
        db_session.add(new_token)
        db_session.commit()
        db_session.close()
        print('Success')
    except Exception as e:
        print('Error: ', e)
        db_session.rollback()
    finally:
        db_session.close()


def delete_token(args):
    db_session = DB.create_session()
    if len(args) != 1:
        print('Wrong args number. Right args are: <token_id>')
        db_session.close()
        return

    try:
        db_session.execute(text('DELETE FROM RegisterToken WHERE ID_RegisterToken = ' + args[0]))
        db_session.commit()
        db_session.close()
        print('Success')
    except Exception as e:
        print('Error: ', e)
        db_session.rollback()
    finally:
        db_session.close()


def delete_all_tokens(args):
    db_session = DB.create_session()
    try:
        db_session.execute(text('DELETE FROM RegisterToken'))
        db_session.commit()
        db_session.close()
        print('Success')
    except Exception as e:
        print('Error: ', e)
        db_session.rollback()
    finally:
        db_session.close()
