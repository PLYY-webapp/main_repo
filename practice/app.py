import database as db
from flask import Flask, jsonify, json

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/plyy')
def plyy():
    query = "SELECT * FROM PLYY"
    plyy = db.get_query(query)
    return jsonify(plyy)


@app.route('/api/plyyList')
def plyyList():
    return app.send_static_file('plyy.html')


if __name__=='__main__':
    app.run(debug=True)