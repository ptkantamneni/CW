from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/signup', methods=['POST'])
def login():
    if request.method == 'POST':
        return perform_signup()
 
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return perform_login()
    
@app.route('/getUserData', methods=['POST'])
def login():
    if request.method == 'POST':
        return perform_login()
 

