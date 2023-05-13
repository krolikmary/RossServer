
import Model
from collections import namedtuple

from loguru import logger as lg
from flask import Flask, render_template, url_for, redirect, request


app = Flask(__name__)

Server = namedtuple('ID', 'ID port protocol')
servers = Model.ServersModel("127.0.0.1")
servers.run()
servers.add_tslumd(7355)
key = 0


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', servers=servers.get_descriptors())


@app.route('/add_message', methods=['POST'])
def add_message():

    port = request.form['port']
    protocol = request.form['protocol']
    lg.debug(f"Got protocol {protocol}")
    if port < "0" or port > "65536":
        return redirect(url_for('main'))
    else:
        if protocol == "sound":
            servers.add_sound("../sounds/")
        if protocol == "TSL UMD v3.1":
            servers.add_tslumd(port)
        if protocol == "JSON":
            servers.add_json(port)

        return redirect(url_for('main'))


@app.route('/delete', methods=['POST'])
def delete():
    lg.debug(str(request.form))
    servers.delete_server(int(request.form["servIndex"]))
    return redirect(url_for('main'))


app.run(debug=True)