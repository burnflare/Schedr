from app import app

@app.route('/')
def check_if_logged_in():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in' 

@app.route('/user/<username>')
def profile(username):
    return 'User name is %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # abort(401)
    return 'Post %d' % post_id

@app.route('/login', methods=['GET', 'POST'])
def login():
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
