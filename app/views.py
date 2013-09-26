from app import app, db
from flask import url_for, request, abort, session, redirect, escape, render_template, jsonify, json
from pprint import pprint

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

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

@app.route('/event/', methods=['POST']) #TODO: change to POST
def save_event_details():
    # event_data = json.loads(request.form['data'])
    # data = request.form.get('data')
    # ss = event_data['recipients']
    event_dict = {
    "recipients" : "a@gmail.com,b@gmail.com,c@gmail.com",
    "name" : "group meeting",
    "venue" : "LT7A",
    "date": "2013-08-16",
    "timeslot": "2",
    "duration": "2"
    }
    #n = json.dumps(json_dict)
    #json_object = json.loads(n)
    #pprint (json_dict)

    #TODO: use escape
    
    if 'creator_id' in session:
        creator_id = session['creator_id']
    else:
        creator_id = 0
    
    event_recipients = event_dict['recipients']
    event_name = event_dict['name']
    event_venue = event_dict['venue']
    suggested_date = event_dict['date']
    suggested_time = event_dict['timeslot']
    duration = event_dict['duration']

    newMeeting = Meetings(creator_id, event_recipients, event_name, event_venue, suggested_date, suggested_time, duration)
    db.session.add(newMeeting)
    db.session.commit()
    return 'Post %r' % 'meeting added successfully'

@app.route('/event/<int:user_id>')
def get_event_details(user_id):
    event_details = {}
    if user_id:
        existing_meetings = Meetings.query.filter_by(creator_id = user_id).all()
        for i in range(len(existing_meetings)):
            event_details[i] = row2dict(existing_meetings[i])    
        #pprint(existing_meetings[0].event_name)
        #pprint(event_details)

        result = jsonify(a = event_details)
        pprint(result)

    return result

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        if column.name is 'suggested_date' or column.name is 'finalized_date':
            continue
        
        d[column.name] = getattr(row, column.name)

    return d

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

def call_google_oauth():
    is_successful = 1
    f_name = 'chinab'
    l_name = 'chugh'
    email = 'chinab91@mail.com'
    oAuth_access = '1234DQ31R3'
    oAuth_token = '1DWQ13RQ3R'
    return is_successful, f_name, l_name, email, oAuth_access, oAuth_token

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class User(db.Model):
    #db.Model is my database
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(255))
    l_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    oAuth_access = db.Column(db.String(255))
    oAuth_token = db.Column(db.String(255))
    
    def __init__(self, f_name=None, l_name=None, email=None, oAuth_access=None, oAuth_token=None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.oAuth_access = oAuth_access
        self.oAuth_token = oAuth_token

    def __repr__(self):
        return '<Id %r>' % (self.user_id)


class Meetings(db.Model):
    #db.Model is my database
    __tablename__ = 'meetings'
    meetings_id = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer)
    event_recipients = db.Column(db.String(255))
    event_name = db.Column(db.String(255))
    event_venue = db.Column(db.String(255))
    suggested_date = db.Column(db.Date)
    suggested_time = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    finalized_date = db.Column(db.Date)
    finalized_time = db.Column(db.Integer)
    
    def __init__(self, creator_id=None, event_recipients=None, event_name=None, event_venue=None, suggested_date=None, suggested_time=None, 
                 duration=None):
        self.creator_id = creator_id
        self.event_recipients = event_recipients
        self.event_name = event_name
        self.event_venue = event_venue
        self.suggested_date = suggested_date
        self.suggested_time = suggested_time
        self.duration = duration
        #self.finalized_date = finalized_date
        #self.finalized_time = finalized_time

    def __repr__(self):
        return '<Id %r>' % (self.meetings_id)


