from app import db

class User(db.Model):
    #db.Model is my database
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(255))
    l_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    
    def __init__(self, f_name=None, l_name=None, email=None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email

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
    suggested_date = db.Column(db.Text)
    suggested_time = db.Column(db.Text)
    duration = db.Column(db.Integer)
    finalized_date = db.Column(db.String(255))
    finalized_time = db.Column(db.String(255))
    
    def __init__(self, creator_id=None, event_recipients=None, event_name=None, event_venue=None, suggested_date=None, suggested_time=None, 
                 duration=None):
        self.creator_id = creator_id
        self.event_recipients = event_recipients
        self.event_name = event_name
        self.event_venue = event_venue
        self.suggested_date = suggested_date
        self.suggested_time = suggested_time
        self.duration = duration
        self.finalized_date = ""
        self.finalized_time = ""

    def __repr__(self):
        return '<Id %r>' % (self.meetings_id)


class Schedule(db.Model):
    #db.Model is my database
    __tablename__ = 'schedule'
    schedule_id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(255))
    time = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    meeting_id = db.Column(db.Integer)
    
    def __init__(self, date=None, time=None, user_id=None, availability=None, meeting_id=None):
        self.date = date
        self.time = time
        self.user_id = user_id
        self.availability = availability
        self.meeting_id = meeting_id

    def __repr__(self):
        return '<Id %r>' % (self.schedule_id)