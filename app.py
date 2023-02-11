from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session

app = Flask(__name__)

# Adding session for user
app.config["SESSION_PERMANENT"] = False #allow it to expire
app.config["SESSION_TYPE"] = "filesystem" #store the session locally
Session(app)

def validate_user(email, password):
    print("validating user...")
    user = {}

    conn = sqlite3.connect('./static/data/activity_tracker.db')
    curs = conn.cursor()
    #get all columns if there is a match
    result  = curs.execute("SELECT name, email, phone FROM users WHERE email=(?) AND password= (?)", [email, password])
  
    for row in result:
       user = {'name': row[0],  'email': row[1], 'phone': row[2]}
         
    conn.close()
    return user


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
    rows = curs.execute("SELECT rowid, * from users")
    for row in rows:
        user = {'rowid': row[0],
                'name' : row[1], 
                'email': row[2],
                'phone': row[3],
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
    data ={}
    if session.get("name"):
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

@app.route('/login_user' , methods=['POST'])
def login_user():

    email = request.form['email']
    password = request.form['password']

    data = {}
    user = validate_user(email, password)

    if user:
       
        data = {
            "name": user["name"],
            "phone": user["phone"]
        }

        #set the user session
        session["name"] = user["name"]

        #load home if there is a user, along with data.
        return render_template('home.html', data=data)
         

    else: 
        error_msg = "Login failed"

        data = {
            "error_msg": error_msg
        }
        #no user redirects back to the main login page, with error msg.
        return render_template('index.html', data=data)



@app.route('/post_user' , methods=['POST'])
def post_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    pw = request.form['password']
    
    store_user(name, email, phone, pw)
    users = get_all_users()
    # print(users)
    #get the last user entered
    new_user = users.pop()

    return render_template('index.html', user=new_user)

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')