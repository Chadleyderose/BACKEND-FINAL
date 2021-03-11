from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime
from flask_cors import CORS


def init_sqlite_db():
    connection = sqlite3.connect('stock.db')
    connection.execute('CREATE TABLE IF NOT EXISTS items (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Name" TEXT NOT NULL,"Type" TEXT NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS Users (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Username" TEXT NOT NULL,"Password" TEXT NOT NULL, "Is-Admin" TEXT NOT NULL)')
    connection.execute('CREATE TABLE IF NOT EXISTS Item_Quantity (	"id"INTEGER PRIMARY KEY AUTOINCREMENT,"Item_id" TEXT NOT NULL,"Quantity" INTEGER)')
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
                cur = conn.cursor()
                conn.row_factory = dict_factory
                cur.execute("INSERT INTO Users(Username,Password) VALUES(?,?)", (Username,Password))
                conn.commit()
                msg = 'Record added'

        except Exception as x:
            msg = 'error'+ str(x)
            
        finally:
            return{'msg':msg}    

@app.route('/users/', methods=['GET'])
def show_users():
        with sqlite3.connect("stock.db") as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users")
            data=cursor.fetchall()
        return jsonify(data)

@app.route('/new-items/', methods=['POST'])
def add_items():
    if request.method== "POST":
        msg=None
        try:
            post_data = request.get_json()
            Name = post_data['Name']
            Type = post_data['Type']

            with sqlite3.connect('stock.db') as conn:
                cur = conn.cursor()
                conn.row_factory = dict_factory
                cur.execute("INSERT INTO items(Name,Type) VALUES(?,?)", (Name,Type))
                conn.commit()
                msg  = "Item added"
        except Exception as x:
            msg = 'error'+ str(x)
        finally:
            return{'msg':msg}    
 

@app.route('/items/', methods=['GET'])
def show_items():
    with sqlite3.connect("stock.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Items")
        data = cursor.fetchall()
    return jsonify(data)

@app.route('/new-item-qty/', methods=['POST'])
def add_item_qty():
    if request.method== "POST":
        msg=None
        try:
            post_data = request.get_json()
            Item_id = post_data['Item_id']
            Quantity = post_data['Quantity']

            with sqlite3.connect('stock.db') as conn:
                cur = conn.cursor()
                conn.row_factory = dict_factory
                cur.execute("INSERT INTO items(Item_id,Quantity) VALUES(?,?)", (Item_id,Quantity))
                conn.commit()
                msg  = "Item Quantity added"
        except Exception as x:
            msg = 'error'+ str(x)
        finally:
            return{'msg':msg}   

@app.route('/item-qty/', methods=['GET'])
def show_item_quantity():
    with sqlite3.connect("stock.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Item_Quantity")
        data = cursor.fetchall()
    return jsonify(data)


if __name__ == ('__main__'):
    app.run(debug=True)
