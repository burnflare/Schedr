from app import app, db
from flask import url_for, request, abort, session, redirect, escape, render_template

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login/')
def login():
    is_successful, f_name, l_name, email, oAuth_access, oAuth_token = call_google_oauth()
    if is_successful == 1:
        u = User(f_name, l_name, email, oAuth_access, oAuth_token)
        db.session.add(u)
        db.session.commit()
    return '1'

@app.route('/schedule/<id>', methods=['GET','POST'])
def manage_user_schedule():
    return 1

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # abort(401)
    return 'Post %d' % post_id

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
    email = 'chinab91@gmail.com'
    oAuth_access = '1234DQ31R3'
    oAuth_token = '1DWQ13RQ3R'
    return is_successful, f_name, l_name, email, oAuth_access, oAuth_token

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key = True)
    fName = db.Column(db.String(255))
    lName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    oAuth_access = db.Column(db.String(255))
    oAuth_token = db.Column(db.String(255))
    
    def __init__(self, f_name=None, l_name=None, email=None, oAuth_access=None, oAuth_token=None):
        self.fName = f_name
        self.lName = l_name
        self.email = email
        self.oAuth_access = oAuth_access
        self.oAuth_token = oAuth_token

    def __repr__(self):
        return '<User %r>' % (self.email)






