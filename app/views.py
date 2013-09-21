from app import app, db
from flask import url_for, request, abort, session, redirect, escape

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login/')
def login():
    isSuccessful = call_google_oauth();
    if isSuccessful == 1:
        return 1

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
    return 1;

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'





