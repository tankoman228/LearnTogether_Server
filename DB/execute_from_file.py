import os

from sqlalchemy import text


def executor(file_path, Ses):

    try:
        file_path = os.path.join(*file_path.split('\\'))

        f = open(file_path, 'r')
        sqls = f.read().split(';')
        f.close()

        try:
            sqls.remove('')
        except:
            pass

        for sql in sqls:
            Ses.execute(text(sql))

        Ses.commit()

    except Exception as e:
        print(f'Script {file_path} error. '
              f'Maybe, this file does not exists or damaged. \nError: {e}')
