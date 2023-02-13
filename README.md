# flask-activity-tracker

Demo app for using SQLite with Flask on a Raspberry Pi. 

This version includes the ability to edit activities. 

From the Home screen, a user can now click on each activity tile and go to the `edit.html` screen where the rowid of the activity is used to load the UI. Then the user can make changes and edit the content. 

in `app.py` there is now an `update_activity` function that uses the UPDATE SQL commands to make changes to the database.

### JavaScript
This version also includes a bi of JavaScript to make the `Add Activity` container hide and show if user is entering information. 

NOTE: No validation of values or deletion of activities is yet available. 
