from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql-service'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'feedbackdb'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']
    message = request.form['message']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO feedback(name,email,department,message)
        VALUES(%s,%s,%s,%s)
    """, (name,email,department,message))

    mysql.connection.commit()
    cur.close()

    return redirect('/records')

@app.route('/records')
def records():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedback")
    data = cur.fetchall()
    cur.close()

    return render_template('records.html', records=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
