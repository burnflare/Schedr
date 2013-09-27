from app import app, db
from flask import url_for, request, abort, session, redirect, escape, render_template, jsonify, json
from pprint import pprint
from models import User, Meetings, Schedule
import csv

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login/', methods=['POST'])
def login():
    #is_successful, f_name, l_name, email = call_google_oauth()
    pprint('hiiiii' + request.data)
    google_ouath_dict = json.loads(request.data)
    f_name = google_ouath_dict['fname']
    l_name = google_ouath_dict['lname']
    email = google_ouath_dict['email']

    #if is_successful == 1:
    existingUsers = User.query.filter_by(email = email).first()
    if existingUsers is None:
        newUser = User(f_name, l_name, email)
        db.session.add(newUser)
        db.session.commit()
        session['creator_id'] = newUser.user_id
    else:
        session['creator_id'] = existingUsers.user_id

    return jsonify(user_id = session['creator_id'])


@app.route('/specific_event/<int:meeting_id>', methods=['GET'])
def get_event_details(meeting_id):
    current_meeting = Meetings.query.filter_by(meetings_id = meeting_id).first()
    pprint(current_meeting.meetings_id)
    current_meeting_dict = row2dict(current_meeting)
    result = jsonify(current_meeting = current_meeting_dict)
    #session.pop('meeting_id', None)
    return result


@app.route('/event/', methods=['POST'])
def process_event_details():
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0

    if creator_id != 0:
        event_dict = json.loads(request.data)

        #TODO: use escape
        event_recipients = ",".join(event_dict['recipients'])
        event_name = event_dict['name']
        event_venue = event_dict['venue']
        suggested_date = ",".join(event_dict['date'])
        suggested_time = ",".join(event_dict['timeslot'])
        duration = 0 #TODO: event_dict['duration']

        newMeeting = Meetings(creator_id, event_recipients, event_name, event_venue, suggested_date, suggested_time, duration)
        db.session.add(newMeeting)
        db.session.commit()
        #session['meeting_id'] = newMeeting.meetings_id
        return 'Post meeting added successfully'
    return 'Please login successfully'


@app.route('/admin/', methods=['GET'])
def get_admin_details():
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0

    creator_id = 18 #TODO: comment this off
    count = 0
    event_details = {}
    if creator_id:
        #existing_meetings = Meetings.query.filter_by(creator_id = creator_id).all()
        existing_meetings = Meetings.query.all()
        for i in range(len(existing_meetings)):
            db_creator_id = existing_meetings[i].creator_id
            if db_creator_id == creator_id:
                event_details['meeting_' + str(count)] = row2dict(existing_meetings[i])
                count = count + 1
                continue

            db_event_recipients = existing_meetings[i].event_recipients
            db_event_recipients_list = db_event_recipients.split(',')
            for j in db_event_recipients_list:
                user_id_in_recipient = User.query.filter_by(email = j).first()
                if user_id_in_recipient is not None:
                    db_user_id = user_id_in_recipient.user_id
                    if db_user_id == creator_id:
                        event_details['meeting_' + str(count)] = row2dict(existing_meetings[i])
                        count = count + 1
                        continue
        #pprint(existing_meetings[0].event_name)
    result = jsonify(event_list = event_details)
    return result


@app.route('/schedule/<int:meeting_id>', methods=['GET', 'POST'])
def manage_user_schedule(meeting_id):
    pprint('hi')
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0
    if creator_id != 0:
        meeting_schedule = json.loads(request.data)
        selected_timings = meeting_schedule['selected_timings']
        for i in selected_timings:
            availability = 1
            pprint(i)
            selected_datetime = i.split('_')
            pprint(selected_datetime)
            time = selected_datetime[0]
            date = selected_datetime[1]
            newSchedule = Schedule(date, time, creator_id, availability, meeting_id)
            db.session.add(newSchedule)
            db.session.commit()
    return 'successful'

@app.route('/logout')
def logout():
    session.pop('username', None)
    app.logger.debug('logging out')
    return redirect(url_for('check_if_logged_in'))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

def call_google_oauth():
    is_successful = 1
    f_name = 'chinab'
    l_name = 'chugh'
    email = 'chinab91@mail.com'
    return is_successful, f_name, l_name, email

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        #if column.name is 'event_recipients':
        #loc    d[column.name] = row.event_recipients.split(',')        
            #continue
        d[column.name] = getattr(row, column.name)
        
    return d

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
