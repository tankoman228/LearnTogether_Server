from sqlalchemy import text
from sqlalchemy.orm import Session


def drop_create(Ses: Session):
    try:
        f = open('DB\\DB_Queries\\DropCreate.sql', 'r')
        sqls = f.read().split(';')
        f.close()

        try:
            sqls.remove('')
        except:
            pass

        f2 = open('DB\\DB_Queries\\FillBasic.sql', 'r')
        sqls2 = f2.read().split(';')
        f2.close()

        try:
            sqls2.remove('')
        except:
            pass
    except Exception as e:
        print(f'Can\'t recreate database from script. '
              f'Maybe, this file does not exists or damaged. \nError: {e}')
        return

    try:
        for sql in sqls:
            Ses.execute(text(sql))
        for sql2 in sqls2:
            Ses.execute(text(sql2))
        Ses.commit()

    except Exception as e:
        print('Your SQL script contained some errors, try recreate_db using right script. Error is: \n', e)