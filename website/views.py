from flask import Blueprint, render_template, request
import sqlite3
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/overview', methods=['GET'])
def overview():
    fighter_name = request.args.get('octo_input')

    #Determine the full path to the desktop directory
    desktop_path = os.path.expanduser("~/Desktop")
    db_file_path = os.path.join(desktop_path, "octovaultdb")

    #Establish a connection to the SQLite database using the full path
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    if is_event_name(fighter_name):
        event_name = fighter_name.lower()
        if "vs" in event_name and "vs." not in event_name:
            event_name = event_name.replace("vs", "vs.")
        
        event_name_query = "SELECT DISTINCT eventname, eventdate FROM fights WHERE LOWER(eventname) LIKE ?"
        search_pattern = f"%{event_name}%"
        cursor.execute(event_name_query, (search_pattern,))
        results = cursor.fetchall()
        if results:
            event_name = results[0][0]
            event_date = results[0][1]
            fights_query = "SELECT * FROM fights WHERE eventname = ?"
            cursor.execute(fights_query, (event_name,))
            fights = cursor.fetchall()

            #Create dictionary for rendering fight and event data
            event_data = {
                "event_name": event_name,
                "event_date": event_date,
                "fights": fights
            }

            return render_template("eventOverview.html", **event_data)
        else:
            event_data = {
                "event_name": 'Event not Found',
                "fights": []
            }
            return render_template("eventOverview.html", **event_data)



    #Query to retrive basic fighter info from the database
    fighter_info_query = "SELECT * FROM fighters WHERE LOWER(first_name) = ? AND LOWER(last_name) = ?"
    first_name, last_name = fighter_name.split()
    first_name = first_name.lower()
    last_name = last_name.lower()
    fighter_params = (first_name, last_name)

    cursor.execute(fighter_info_query, fighter_params)
    fighter_info = cursor.fetchall()

    #Query to retrieve fights the fighter has taken place in
    fights_query = "SELECT * FROM fights WHERE LOWER(fighter1) = ? OR LOWER(fighter2) = ?"
    fights_params = (fighter_name.lower(), fighter_name.lower())
    cursor.execute(fights_query, fights_params)
    fighter_fights = cursor.fetchall()

    #Closes connection to db
    cursor.close()
    conn.close()

    #Following block handles if a fighter is typed in
    if fighter_info:
        fighter_data = {
            'fighter_name': f"{fighter_info[0][0]} {fighter_info[0][1]}",
            'fighter_nickname': fighter_info[0][2],
            'wins': fighter_info[0][7],
            'losses': fighter_info[0][8],  
            'draws': fighter_info[0][9],  
            'height': fighter_info[0][3],
            'weight': fighter_info[0][4],
            'reach': fighter_info[0][5],
            'stance': fighter_info[0][6],
            'previous_fights': fighter_fights
        }
    else:
        #Handle the case where the fighter is not found
        fighter_data = {
            'fighter_name': 'Fighter Not Found',
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'previous_fights': []
        }

    return render_template("overview.html", **fighter_data)


def is_event_name(input):
    if "ufc" in input.lower():
        return input
    elif "vs" in input.lower():
        return input
    return False
