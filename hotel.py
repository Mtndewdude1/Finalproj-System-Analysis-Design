from flask import Flask, redirect, url_for, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('welcome.htm')

@app.route('/bookaroom')
def bookaroom():
	return render_template('booking.htm')

@app.route("/addbookingrecord", methods = ["POST", "GET"])
def addbookingrecord():
    if request.method == "POST":
        name = request.form["name"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]
        roomtype = request.form["roomtype"]

        cmd = "INSERT INTO hotel (name, checkin, checkout, roomtype) VALUES ('{0}', '{1}', '{2}', '{3}')".format(name, checkin, checkout, roomtype)

        with sql.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            # msg = "Customer data successfully saved."
            return render_template("confirmed.htm", name=name, checkin=checkin, checkout=checkout) #, msg = msg

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pswd = request.form['password']
        if user == 'manager' and pswd == 'hotelManager18':
#            return render_template('list_bookings.htm', name=user)
                conn = sql.connect("database.db")
                conn.row_factory = sql.Row

                cmd = "SELECT * FROM hotel"
                cur = conn.cursor()
                cur.execute(cmd)
                rows = cur.fetchall()
                conn.close()
                return render_template("list_bookings.htm", rows = rows)
        else:
            return render_template('rejected_login.htm', name=user)
    else:
        return render_template('login.htm')


if __name__ == "__main__":
	app.run()