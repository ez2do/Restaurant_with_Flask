from flask import Flask
app = Flask(__name__)

@app.route('/')
def default():
	return "Nhin cc"

@app.route('/user/<user_name>')
def welcomeUser(user_name):
	return "Dm %s" % user_name

@app.route('/user/')
def user_do():
	return "User"

@app.route('/id/<int:user_id>')
def showID(user_id):
	return "Phang ngay con lo %d" % user_id

@app.route('/<random>')
def showRan(random):
	return "Show me %s" % random

@app.route('/hello')
def helloWorld():
	return "Hello World"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)