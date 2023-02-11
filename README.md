# flask-activity-tracker

Demo app for using SQLite with Flask on a Raspberry Pi. This version shows how to create a new user and log in with basic email/password credentials. No validation or user sessions are used. 
The goal of this demo is to show how to store data and retrieve it from a SQLite database.


## Session branch 

This branch adds a Flask user session:
```
from flask_session import Session
```
- New logout() function added to app.py
- `home.html` now uses `session.name` 



A user can also log out from the home.html page. 
If logged in, a user will be redirected home. If not logged in, a user who reaches home, will be redirected to index.html.

