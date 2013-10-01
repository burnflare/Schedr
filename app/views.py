from app import app, db, mail, USERNAME
from flask import url_for, request, abort, session, redirect, escape, render_template, jsonify, json
from pprint import pprint
from models import User, Meetings, Schedule
from flask.ext.mail import Message
import csv

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/testing_email')
def email():
    msg = Message("Invitation to schedule your meeting by ",
                  sender=USERNAME,
                  recipients=['chinab91@gmail.com', 'chinab@jublia.com'])
    msg.body = "hello world"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return 'a'

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
        #user who is coming in again
        existingUsers.f_name = f_name
        existingUsers.l_name = l_name
        db.session.commit()
        session['creator_id'] = existingUsers.user_id

    return jsonify(user_id = session['creator_id'])


@app.route('/specific_event/<meeting_id>', methods=['GET'])
def get_event_details(meeting_id):
    meeting_id += '==='
    decoded_string = meeting_id.decode('base64', 'strict')
    decoded_list = decoded_string.split('&',1)
    meeting_id = decoded_list[0][4:]
    email = decoded_list[1][4:]
    find_user = User.query.filter_by(email = email).first()
    user_id = find_user.user_id


    current_meeting = Meetings.query.filter_by(meetings_id = meeting_id).first()
    pprint(current_meeting.meetings_id)
    current_meeting_dict = row2dict1(current_meeting, user_id)
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
        #event_dict['recipients'] = ['chinab91@gmail.com', 'chinab@jublia.com']
        #TODO: use escape
        event_recipients = ",".join(event_dict['recipients'])
        event_name = event_dict['name']
        event_venue = event_dict['venue']
        suggested_date = ",".join(event_dict['date'])
        suggested_time = ",".join(event_dict['timeslot'])
        duration = 1

        meeting_size = len(event_dict['recipients']) + 1

        newMeeting = Meetings(creator_id, event_recipients, meeting_size, event_name, event_venue, suggested_date, suggested_time, duration)
        db.session.add(newMeeting)
        db.session.commit()

        for each_user_email in event_dict['recipients']:
            new_user = User("", "", each_user_email)
            db.session.add(new_user)
            db.session.commit()

        existing_users = User.query.filter_by(user_id = creator_id).first()
        user_name = existing_users.f_name
        email = existing_users.email

        

        for each_email in event_dict['recipients']:
            email_list = []
            email_list.append(each_email)

            encoded_string = ("mid="+str(newMeeting.meetings_id)+"&eid="+each_email).encode('base64', 'strict')

            msg = Message("Invitation to schedule a meeting with " + user_name,
                sender=USERNAME,
                recipients=email_list)
            msg.body = "hello"
            msg.html = "Hey!<br/><br/>"+user_name+ " has scheduled a meeting called " + event_name + " for either of the dates: " + suggested_date+".<br/><br/> You can confirm your availability via sd.vishnuprem.com/static/calender.html?pid="+encoded_string+". Its very simple to do so with a single click google login and we will schedule a time for you to meet<br/><br/>You will be notifed with the confirmed date/time when everyone submits -  as simple as that :) Thanks!"
            mail.send(msg)

        
        #session['meeting_id'] = newMeeting.meetings_id
        return 'Post meeting added successfully'
    return 'Please login successfully'


@app.route('/admin/')
def get_admin_details():
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0

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


@app.route('/schedule/<meeting_id>', methods=['GET', 'POST'])
def manage_user_schedule(meeting_id):
    val = 0
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0

    has_submitted = 0
    meeting_id += '==='
    decoded_string = meeting_id.decode('base64', 'strict')
    decoded_list = decoded_string.split('&',1)
    meeting_id = decoded_list[0][4:]
    email = decoded_list[1][4:]
    pprint("meeting id is "+meeting_id)
    pprint("email is "+email)

    if creator_id == 0:
        #person is coming in via email
        find_user = User.query.filter_by(email = email).first()
        creator_id = find_user.user_id

    if creator_id != 0:
        does_schedule_exist = Schedule.query.filter_by(user_id = creator_id, meeting_id = meeting_id).all()
        for row in does_schedule_exist:
            has_submitted = 1;
            db.session.delete(row)
            db.session.commit()

        if has_submitted == 0:
            pprint('hasnt submitted')
            existing_meeting = Meetings.query.filter_by(meetings_id = meeting_id).first()
            existing_meeting.count_logged_in = existing_meeting.count_logged_in + 1
            db.session.commit()
        else:
            pprint('has submitted')

        meeting_schedule = json.loads(request.data)
        selected_timings = meeting_schedule['selected_timings']
        for i in selected_timings:
            availability = 1
            pprint(i)
            selected_datetime = i.split('_')
            time = selected_datetime[0]
            date = selected_datetime[1]
            newSchedule = Schedule(date, time, creator_id, availability, meeting_id)
            db.session.add(newSchedule)
            db.session.commit()
        #everyone has submitted, logic to calculate the meeting
        if has_submitted == 0:
            if existing_meeting.meeting_size == existing_meeting.count_logged_in:
                pprint('inside the scheduler')
                val = scheduler(existing_meeting)
    return str(val)

#@app.route('/test_scheduler/')
def scheduler(existing_meeting):
    #existing_meeting = Meetings.query.filter_by(meetings_id = 41).first()
    recipients_in_meeting = []
    event_recipients_list = existing_meeting.event_recipients.split(',')

    for email in event_recipients_list:
        user = User.query.filter_by(email = email).first()
        if user is not None:
            recipients_in_meeting.append(user.user_id)
    creator_availability = Schedule.query.filter_by(meeting_id = existing_meeting.meetings_id, user_id = existing_meeting.creator_id).all()
    for each_availability in creator_availability:
        available_date = each_availability.date
        available_time = each_availability.time
        count = 1
        for event_recipient_id in recipients_in_meeting:
            event_recipient_availability = Schedule.query.filter_by(meeting_id = existing_meeting.meetings_id, user_id = event_recipient_id, date = available_date, time = available_time).first()
            if event_recipient_availability is None:
                break
            else:
                count = count + 1
                if(existing_meeting.meeting_size == count):
                    #meeting scheduled as everyone is fine with that date and time
                    pprint('scheduling a meeting')
                    existing_meeting.finalized_date = available_date
                    existing_meeting.finalized_time = available_time
                    db.session.commit()

                    creator_user = User.query.filter_by(user_id = existing_meeting.creator_id).first()
                    creator_user_email = creator_user.email
                    event_recipients_list.append(creator_user_email)
                    pprint(event_recipients_list)

                    msg = Message("Finalized meeting details - " + existing_meeting.event_name,
                    sender=USERNAME,
                    recipients=event_recipients_list)
                    msg.body = "hello"
                    msg.html = "Hey!<br/><br/>Schedr has finalized a meeting date/time for " + existing_meeting.event_name + ".<br/>We looked at the choices submitted by your team and we consider the best time for you to meet up is on " + available_date + " at " + available_time + ".<br/><br/>Hope your meeting goes great! Continue to use schedr at sd.vishnuprem.com to schedule your life."
                    mail.send(msg)
                    return 1
    return 0


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
        if column.name is 'meetings_id':
            user_id = session['creator_id']
            existing_users = User.query.filter_by(user_id = user_id).first()
            email = existing_users.email
            encoded_string = ("mid="+str(row.meetings_id)+"&eid="+email).encode('base64', 'strict')
            d[column.name] = encoded_string
            continue
        d[column.name] = getattr(row, column.name)
        
    return d

def row2dict1(row, user_id):
    d = {}
    for column in row.__table__.columns:
        if column.name is 'meetings_id':
            existing_users = User.query.filter_by(user_id = user_id).first()
            email = existing_users.email
            encoded_string = ("mid="+str(row.meetings_id)+"&eid="+email).encode('base64', 'strict')
            d[column.name] = encoded_string
            continue
        d[column.name] = getattr(row, column.name)
        
    return d


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
