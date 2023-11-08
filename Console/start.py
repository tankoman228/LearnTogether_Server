from flask import Flask
from flask import jsonify

import FlaskScipts.test_scripts

def real_start(cmd):
    #пока что не работает и виснет

    app = Flask(__name__)
    app.run(debug=True)

    @app.route('/users')
    def fef():
        return jsonify('hfef')