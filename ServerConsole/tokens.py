from sqlalchemy import text

import DB


def tokens(args):
    print('ATTENTION! Tokens must be hidden from other users. Don\'t give screenshot to everyone and '
          'give token for one user only \n')

    print('Tokens list:')
    ts = DB.Ses.query(DB.RegisterToken).all()

    if len(ts) == 0:
        print('<empty>')

    for t in ts:
        print(f'ID: {t.ID_RegisterToken} \t| Group[{t.group.ID_Group}]: {t.group.Name} '
              f'\t| Role[{t.role.ID_Role}]: {t.role.Name} \t |  {t.Text}  |')


def create_token(args):

    if len(args) != 3:
        print('Wrong args number. Right args are: <id_group> <id_role> <token_string>')

    try:
        new_token = DB.RegisterToken(ID_Group=int(args[0]), ID_Role=int(args[1]), Text=args[2])
        DB.Ses.add(new_token)
        DB.Ses.commit()

        print('Success')
    except Exception as e:
        print('Error: ', e)
        DB.Ses.rollback()


def delete_token(args):

    if len(args) != 1:
        print('Wrong args number. Right args are: <token_id>')

    try:
        DB.Ses.execute(text('DELETE FROM `RegisterToken` WHERE `ID_RegisterToken` = ' + args[0]))
        DB.Ses.commit()

        print('Success')
    except Exception as e:
        print('Error: ', e)
        DB.Ses.rollback()


def delete_all_tokens(args):
    try:
        DB.Ses.execute(text('DELETE FROM `RegisterToken`'))
        DB.Ses.commit()

        print('Success')
    except Exception as e:
        print('Error: ', e)
        DB.Ses.rollback()
