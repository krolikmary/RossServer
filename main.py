

from collections import namedtuple


from flask import Flask, render_template, url_for, redirect, request


app = Flask(__name__)

Server = namedtuple('ID', 'ID port protocol')
servers = {}

key = 0

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', servers=servers)



@app.route('/add_message', methods=['POST'])
def add_message(key):
    ID = request.form['ID']
    port = request.form['port']
    protocol = request.form['protocol']
    servers[key] = Server(ID, port, protocol)
    key = key+1
    return redirect(url_for('main'))

@app.route('/delete', methods=['GET'])
def delete(servIndex):
    servers.pop(servIndex)
    return redirect(url_for('main'))