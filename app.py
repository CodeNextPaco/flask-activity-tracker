from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
from datetime import datetime

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
    result  = curs.execute("SELECT rowid, name, email, phone FROM users WHERE email=(?) AND password= (?)", [email, password])
  
    for row in result:
       user = {'rowid': row[0], 'name': row[1],  'email': row[2], 'phone': row[3]}
         
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

def get_all_user_activities(id):
    conn = sqlite3.connect('./static/data/activity_tracker.db')
    curs = conn.cursor()
    activities = [] # will store them in a list
    result = curs.execute("SELECT * from activities WHERE user_id=(?)", (id,))
    for row in result:
        activity = {
                'activity_name' : row[0], 
                'date': row[1],
                'quantity': row[2],
                'description': row[3],
                'type': row[4]
                }
        activities.append(activity)

    conn.close()

    return activities


def store_activity(name, activity_type, desc, user, qty):

    now = datetime.now() # current date and time   
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    conn = sqlite3.connect('./static/data/activity_tracker.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO activities (activity_name, date, quantity, description, user_id, type) VALUES((?),(?),(?),(?),(?),(?))",
        (name, date_time, qty, desc, user, activity_type))
    
    conn.commit()
    conn.close()


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

        #make sure we have the latest ones, after every new one is added
        activities = get_all_user_activities(userid)
        session["activities"] = activities
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
            "phone": user["phone"],
            "id": user["rowid"]
        
        }

        #set the user session
        session["name"] = user["name"]
        session["userid"] = user["rowid"]
        userid = user["rowid"]
        activities = get_all_user_activities(userid)
        session["activities"] = activities

        #load home if there is a user, along with data.
        return render_template('home.html', data=data)
         
    else: 
        error_msg = "Login failed"

        data = {
            "error_msg": error_msg
        }
        #no user redirects back to the main login page, with error msg.
        return render_template('index.html', data=data)

@app.route('/post_activity', methods=['POST'])
def post_activity():
    name = request.form['activity-name']
    activity_type = request.form['activity-type']
    description = request.form['activity-desc']
    quantity = request.form["activity-qty"]
    userid = session["userid"]
    store_activity(name, activity_type, description, userid, quantity)

    user_activities = get_all_user_activities(session['userid'])
    print(user_activities)
    session["activities"] = get_all_user_activities(session['userid'])
     


    return render_template('home.html')




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
    session["userid"] = None
    session["activities"] = None
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')