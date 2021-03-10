from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime
from flask_cors import CORS


def init_sqlite_db():
    connection = sqlite3.connect('stock.db')
    connection.execute('CREATE TABLE IF NOT EXISTS items (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Name" TEXT NOT NULL,"Type" TEXT NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS Users (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Username" TEXT NOT NULL,"Password" TEXT NOT NULL, "Is-Admin" TEXT NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS Item_Quantity (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Item_id" TEXT NOT NULL,"Quantity" INTEGER)')
    connection.execute('CREATE TABLE IF NOT EXISTS Logged_in_users ("id"INTEGER PRIMARY KEY AUTOINCREMENT,"Username" TEXT NOT NULL,"User_Id" INTEGER NOT NULL, "Logged_In" TEXT NOT NULL)')

    print("database stock.db connection was succesfull.")


init_sqlite_db()
app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
@app.route('/new-user/', methods=['POST'])
def add_users():
    if request.method== "POST":
        msg=None
        try:
            post_data = request.get_json()
            Username = post_data['Username']
            Password = post_data['Password']

            with sqlite3.connect('stock.db') as conn:
                cur - con.cursor()
                con.row_factory = dict_factory
                cur.execute("INSERT INTO Users(Username,Password) VALUES(?,?)", (Username,Password))
                con.commit()
                msg "Record added"
        except Exception as x:
            msg = 'error'+ str(x)
        finally:
            return{'msg':msg}    

@app.route('/users/', methods=['GET'])
def show_users():
        with sqlite3.connect("stock.db") as conn:
            con.row_factory = dict_factory
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Users")
            data=cursor.fetchall()
        return jsonify(data)

@app.route('/new-user/', methods=['POST'])
def add_users():
    if request.method== "POST":
        msg=None
        try:
            post_data = request.get_json()
            Username = post_data['Username']
            Password = post_data['Password']

            with sqlite3.connect('stock.db') as conn:
                cur - con.cursor()
                con.row_factory = dict_factory
                cur.execute("INSERT INTO Users(Username,Password) VALUES(?,?)", (Username,Password))
                con.commit()
                msg "Record added"
        except Exception as x:
            msg = 'error'+ str(x)
        finally:
            return{'msg':msg}    


@app.route('/items/', methods=['GET'])
def show_items():
    with sqlite3.connect("stock.db") as conn:
        conn.row_factory = dict_factory
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Items")
        data = cursor.fetchall()
    return jsonify(data)

@app.route('/item-qty/', methods=['GET'])
def show_item_quantity():
    with sqlite3.connect("stock.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Item_Quantity")
        data = cursor.fetchall()
    return jsonify(data)

@app.route('/Logged_in/', methods=['GET'])
def show_Logged_in():
    with sqlite3.connect("stock.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Logged_in_users")
        data = cursor.fetchall()
    return jsonify(data)




if __name__ == ('__main__'):
    app.run(debug=True)
