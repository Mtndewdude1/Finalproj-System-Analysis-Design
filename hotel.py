from flask import Flask, redirect, url_for, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template('welcome.htm')

@app.route('/roombooking')
def roombooking():
	return render_template('booking.htm')

@app.route("/suitebooking", methods = ["POST", "GET"])
def suitebooking():
    if request.method == "POST":
        name = request.form["name"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]
        roomtype = request.form["roomtype"]

        cmd = "INSERT INTO hotel (name, checkin, checkout, roomtype) VALUES ('{0}', '{1}', '{2}', '{3}')".format(name, checkin, checkout, roomtype)

        with sql.connect("hotel.db") as conn:
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            return render_template("confirmation.htm", name=name, checkin=checkin, checkout=checkout)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pswd = request.form['password']
        if user == 'Manager' and pswd == 'Panther$hotel':
                conn = sql.connect("hotel.db")
                conn.row_factory = sql.Row

                cmd = "SELECT * FROM hotel"
                cur = conn.cursor()
                cur.execute(cmd)
                rows = cur.fetchall()
                conn.close()
                return render_template("listRooms.htm", rows = rows)
        else:
            return render_template('manageronly.htm', name=user)
    else:
        return render_template('login.htm')


if __name__ == "__main__":
	app.run()