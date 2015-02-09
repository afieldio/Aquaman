import sqlite3

from flask import Flask, jsonify, request, session, g, redirect, url_for, render_template, flash
# from contextlib import 
import gviz_api
import json


#configuration

DATABASE =  'data.db'
DEBUG = True
SECRET_KEY = 'dev key'
USERNAME = 'admin'
PASSWORD = 'default'
entries = ""

#create application

app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode ='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def show_entries():
	cur = g.db.execute('select * from tempdata order by time asc')
	description = {"id": ("number", "ID"), "Temp": ("number", "temp"), "Time": ("datetime", "time")}
	entries = [(row[2], row[1]) for row in cur.fetchall()]
	# entries = ""
	# for row in cur.fetchall():
	# 	entries += "[{{0}}, {{1}}]".format(row[0], row[1])
	# 	print entries
	data=json.dumps(entries)

	print data


	# print data
	# data_table = gviz_api.DataTable(description)
	# data_table.LoadData(data)

	# json = data_table.ToJSon(columns_order=("id", "Temp", "Time"),order_by="Time")

	# entries=jsonify(results=entries)
	# for row in cur.fetchall():
	# 	print "[{1}, {2}]".format(row[0], row[1])
	return render_template('show_data.html', data=data)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into tempdata (temp, time) values (?, datetime())', [request.form['temp']])
	g.db.commit()
	flash('New Entry Successfull')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))





if __name__ == '__main__':
	app.run()
