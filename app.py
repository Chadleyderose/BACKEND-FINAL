from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime
from flask_cors import CORS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    connection = sqlite3.connect('stock.db')
    connection.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, Username  TEXT, Password TEXT)')
#     connection.execute('CREATE TABLE IF NOT EXISTS kitchen (id INTEGER PRIMARY KEY AUTOINCREMENT, Username  TEXT, Password INT)')
#     connection.execute('CREATE TABLE IF NOT EXISTS equipment (id INTEGER PRIMARY KEY AUTOINCREMENT, Username  TEXT, Password INT)')
#     connection.execute('CREATE TABLE IF NOT EXISTS food (id INTEGER PRIMARY KEY AUTOINCREMENT, Username  TEXT, Password INT)')

    print("database stock.db connection was succesfull.")


init_sqlite_db()

def add_admin():
    username = "admin"
    password = "admin"
    conn = sqlite3.connect('stock.db')
    conn.execute('INSERT INTO Users (Username, Password) VALUES(?, ?)', (username, password))
    conn.commit()
    print("Admin has been created")
    conn.close()


add_admin()


app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/new_user/', methods=['POST'])
def add_users():
    msg=None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            Username = post_data['Username']
            Password = post_data['Password']

            with sqlite3.connect('stock.db') as conn:
                cur = conn.cursor()
                conn.row_factory = dict_factory
                cur.execute("INSERT INTO Users(Username, Password) VALUES(?, ?)", (Username, Password))
                conn.commit()
                msg = Username + 'Record added'

        except Exception as x:
            conn.rollback()
            msg = 'error'+ str(x)
            
        finally:
            conn.close()
            return jsonify(msg)   

@app.route('/users/', methods=['GET'])
def show_users():
    records = []
    try:
        with sqlite3.connect("stock.db") as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users")
            records=cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print("THre was an error fetching" + str(e))
    finally:
        conn.close()
        return jsonify(records)

# @app.route('/kitchen/', methods=['POST'])
# def add_to_kitchen():
#     if request.method== "POST":
#         msg=None
#         try:
#             post_data = request.get_json()
#             Name = post_data['Name']
#             Type = post_data['Type']

#             with sqlite3.connect('stock.db') as conn:
#                 cur = conn.cursor()
#                 conn.row_factory = dict_factory
#                 cur.execute("INSERT INTO kitchen(Name, Type) VALUES(?, ?)", (Name, Type))
#                 conn.commit()
#                 msg  = "Item added"
#         except Exception as x:
#             msg = 'error'+ str(x)
#         finally:
#             return{'msg':msg}    
 

# @app.route('/kitchen_show/', methods=['GET'])
# def show_items():
#     with sqlite3.connect("stock.db") as conn:
#         conn.row_factory = dict_factory
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM kitchen")
#         data = cursor.fetchall()
#     return jsonify(data)

# @app.route('/equipment/', methods=['POST'])
# def add_to_kitchen():
#     if request.method== "POST":
#         msg=None
#         try:
#             post_data = request.get_json()
#             Name = post_data['Name']
#             Type = post_data['Type']

#             with sqlite3.connect('stock.db') as conn:
#                 cur = conn.cursor()
#                 conn.row_factory = dict_factory
#                 cur.execute("INSERT INTO equipment(Name, Type) VALUES(?, ?)", (Name, Type)")
#                 conn.commit()
#                 msg  = "Item added"
#         except Exception as x:
#             msg = 'error'+ str(x)
#         finally:
#             return{'msg':msg}    
 
# @app.route('/Food/', methods=['POST'])
# def Food_items():
#     if request.method== "POST":
#         msg=None
#         try:
#             post_data = request.get_json()
#             Name = post_data['Name']
#             Type = post_data['Type']

#             with sqlite3.connect('stock.db') as conn:
#                 cur = conn.cursor()
#                 conn.row_factory = dict_factory
#                 cur.execute("INSERT INTO Food(Name, Type) VALUES(?, ?)", (Name, Type)")
#                 conn.commit()
#                 msg  = "Item added"
#         except Exception as x:
#             msg = 'error'+ str(x)
#         finally:
#             return{'msg':msg}    
 

# @app.route('/food/', methods=['GET'])
# def show_items():
#     with sqlite3.connect("stock.db") as conn:
#         conn.row_factory = dict_factory
#         cursor.execute("SELECT * FROM food")
#         data = cursor.fetchall()
#     return jsonify(data)


if __name__ == ('__main__'):
    app.run(debug=True)
