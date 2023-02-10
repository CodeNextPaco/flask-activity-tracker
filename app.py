from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def store_user(name, email, phone, pw):
    conn = sqlite3.connect('./static/data/activity_tracker.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO users (name, email, phone, password) VALUES((?),(?),(?),(?))",
        (name, email, phone, pw))



    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect('./static/data/activity_tracker.db')
    curs = conn.cursor()
    all_users = [] # will store them in a list
    rows = curs.execute("SELECT * from users")
    for row in rows:
        user = {'name' : row[0], 
                'email': row[1],
                'phone': row[2],
                }
        all_users.append(user)

    conn.close()

    return all_users






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():

    return render_template('home.html')

@app.route('/post_user' , methods=['POST'])
def post_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    pw = request.form['password']
    
    store_user(name, email, phone, pw)

    users = get_all_users()
    print(users)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')