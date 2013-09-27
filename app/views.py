from app import app, db
from flask import url_for, request, abort, session, redirect, escape, render_template, jsonify, json
from pprint import pprint
from models import User, Meetings

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login/', methods=['POST'])
def login():
    #is_successful, f_name, l_name, email = call_google_oauth()
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
def get_event_details():
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

@app.route('/schedule/', methods=['GET', 'POST'])
def manage_user_schedule():
    if request.method == 'POST':
        session['username']=request.form['username']
        return redirect(url_for('check_if_logged_in'))
    else:
        return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        '''

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
        #if column.name is 'finalized_date':
            #d[column.name] = row.finalized_date.isoformat()        
            #continue
        d[column.name] = getattr(row, column.name)
        
    return d

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
