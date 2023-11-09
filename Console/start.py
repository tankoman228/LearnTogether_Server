from flask import Flask
from flask import jsonify

from threading import Thread

def real_start(cmd):
    t = Thread(target=__start_me_in_other_thread)
    t.daemon = True
    t.start()


def __start_me_in_other_thread():
    app = Flask(__name__)

    @app.route('/')
    def fef():
        return jsonify('hfef')

    app.run(debug=False)