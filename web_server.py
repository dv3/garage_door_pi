#!/usr/bin/python3
#
#
#

import time
import datetime
import logging
import hashlib
import config as c
import garagelib as p
from flask import Flask, flash, redirect, request, render_template, url_for, session, escape, jsonify
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = c.FLASKSECRET

#---------------------

from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')

def create_app():
    app = Flask(__name__)
    # set up the app here
    # for example, register a blueprint
    from my_app.users import bp
    app.register_blueprint(bp)
    return app

@bp.route('/')
def index():
    return render_template('users/index.html')

#-----------------------
@app.route('/')
def index():
    if 'username' in session:
        sensors = p.readSensors()

        for i in range(len(sensors)):
            sensors[i] = p.sensorValueToText(sensors[i])

        timeStamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        data = {'s': sensors, 'ts': timeStamp, 'user': escape(session['username'])}
        return render_template('index.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/trigger')
def trigger():
    if 'username' in session:
        door = request.args.get('door', default = 1, type = int)
        logging.info("Triggering door: " + str(door))
        client.publish("garage/door/trigger", door)
        return jsonify(True)
    else:
        return redirect(url_for('login'))


@app.route('/logs/main')
def mainlogs():
    if 'username' in session:
        f = open(c.BASEPATH + '/logs/main.log', 'r')
        logs = p.tail(f, 100)
        data = {'logs': logs}
        return render_template('logs.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/logs/web')
def weblogs():
    if 'username' in session:
        f = open(c.BASEPATH + '/logs/web.log', 'r')
        logs = p.tail(f, 100)
        data = {'logs': logs}
        return render_template('logs.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from submitted form
        userName = escape(request.form['username'])
        passWord = escape(request.form['password'])
        # Convert password to hash and compare to stored hash
        passWordHash = hashlib.sha256(passWord.encode('utf-8')).hexdigest()
        if userName == c.USERNAME and passWordHash == c.USERHASH:
            session['username'] = 'admin'
            return redirect(url_for('index'))
        else:
            time.sleep(2)
            session.pop('username', None)
            flash('Sorry. Better luck next time.', 'danger')
    else:
        flash('Please enter your details.', 'info')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove username from the session
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)