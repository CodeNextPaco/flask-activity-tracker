# flask-activity-tracker

Demo app for using SQLite with Flask on a Raspberry Pi. This version now includes the ability to create new activities. 

A user who logs in will now be able to create a new activity from the `home.html` page. The activity will also save
a reference to the current userID, which is obtained from the SQLite `rowid` that each new row includes by default. 

This will allow the association of activiites to users, so only users will be able to see their own activities. 

Session now also now keep track of `session["activities"]` that are obtained by querying the database with `get_all_user_activites(id)` which take the session id as an argument.   
