from app import app, db
from flask import url_for, request, abort, session, redirect, escape, render_template, jsonify, json
from pprint import pprint
from models import User, Meetings

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login/')
def login():
    is_successful, f_name, l_name, email, oAuth_access, oAuth_token = call_google_oauth()
    if is_successful == 1:
        existingUsers = User.query.filter_by(email = email).first()
        if existingUsers is None:
            newUser = User(f_name, l_name, email, oAuth_access, oAuth_token)
            db.session.add(newUser)
            db.session.commit()
            session['creator_id'] = newUser.user_id
            return jsonify(test = newUser.user_id)
        else:
            session['creator_id'] = existingUsers.user_id    
            return 'user already exists'
    return 'not successful'

@app.route('/schedule/<id>', methods=['GET','POST'])
def manage_user_schedule():
    return 1

@app.route('/event/', methods=['GET', 'POST'])
def process_event_details():
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0

    if request.method == 'POST':
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
        return 'Post %r' % 'meeting added successfully'

    else:
        if creator_id != 0:
            event_details = {}
            existing_meetings = Meetings.query.filter_by(creator_id = creator_id).all()
            for i in range(len(existing_meetings)):
                creator_id = existing_meetings[i].creator_id
                creator = User.query.filter_by(user_id = creator_id).first()
                f_name = creator.f_name
                l_name = creator.l_name
                full_name = f_name + " " + l_name
                print full_name

                event_details['meeting_'+str(i)] = row2dict(existing_meetings[i]) + full_name #TODO: think of a way to remove meeting0
                #event_details = dict(row2dict(existing_meetings[i]).items())
            #pprint(existing_meetings[0].event_name)
            pprint(event_details)

            result = jsonify(event_list = event_details)
            pprint(result)
            return result

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
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
    oAuth_access = '1234DQ31R3'
    oAuth_token = '1DWQ13RQ3R'
    return is_successful, f_name, l_name, email, oAuth_access, oAuth_token

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        if column.name is 'finalized_date':
            continue        
        d[column.name] = getattr(row, column.name)
    return d

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
