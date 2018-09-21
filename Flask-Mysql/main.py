from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'heena'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)



@app.route('/', methods=['GET', 'POST'])
def submit():
	if request.method == 'POST':
		userDetails = request.form
		name = userDetails['name']
		email = userDetails['email']
		conn = mysql.connect()
		curs = conn.cursor()
		curs.execute("insert into testusers(name, email) values(%s, %s)", (name, email))
		conn.commit() 
		conn.close()
		return redirect('/users')

	return render_template('test.html')


@app.route('/users')
def users():
	conn = mysql.connect()
	curs = conn.cursor()
	resultValue = curs.execute("select * from testusers")
	print("resultValue",resultValue)
	if resultValue > 0:
		userDetails = curs.fetchall()
		return render_template('users.html', userDetails=userDetails)
	conn.close()

if __name__=="__main__":
	app.run(debug=True)
