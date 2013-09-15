from app import app

"""url routing home page """
@app.route('/')
@app.route('/index')
def homepage():
	return 'Hello World!'