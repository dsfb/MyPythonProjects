import os
import re
import sys

from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regex = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    result = db.Column(db.Boolean)

    def __repr__(self):
        return '<Record: {} {}>'.format(self.regex, self.result)


def recreate_db():
    db.drop_all()
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        regex = request.form.get('regex')
        text = request.form.get('text')
        the_result = re.match(regex, text) is not None
        rec = Record()
        rec.regex = regex
        rec.text = text
        rec.result = the_result
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for('result', result_id=rec.id))


@app.route('/result/<int:result_id>/')
def result(result_id):
    the_result = Record.query.get(int(result_id))
    return render_template("result.html", result=the_result)


@app.route('/history/')
def history():
    the_results = Record.query.all()[::-1]
    return render_template('history.html', results=the_results)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        recreate_db()
        app.run(host=arg_host, port=arg_port)
    else:
        recreate_db()
        app.run(debug=True, use_reloader=True)
