import argparse
from flask import Flask, make_response, send_file, request, redirect


parser = argparse.ArgumentParser(description='Run an HTTPS server')
parser.add_argument('-p', '--port', type=int, default=8000, help='port number to listen on')
parser.add_argument('-k', '--keyfile',type=str, default="vulserver.key", help='TLS key file')
parser.add_argument('-c', '--certfile', type=str, default="vulserver.pem", help='TLS cert file')
args = parser.parse_args()

PORT  = args.port
key = args.keyfile
cert = args.certfile

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def index():
    return '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Login</title>
  </head>
  <body>
    <form action="/login" method="post">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required><br>    
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required><br>     
      <input type="submit" value="Login">
    </form>
  </body>
</html>
    '''
#page 1, login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        resp = make_response(redirect('/content'))
        resp.set_cookie('session cookie', 'XXXXXCookieSetAfterUserLoginXXXXX')
        resp.set_cookie('httponly cookie', value='SameSite=NoneHttponly', httponly=True,samesite='None',secure=True)
        resp.set_cookie('samesite Lax', value='Samesite=LaxNooooHttponly', samesite='lax')
        resp.set_cookie('samesite strict', value='Samesite=StrictNooooHttponly', samesite='strict')
        return resp
    else:
        return redirect('/login')
    
#page 2, content after login

@app.route('/')
@app.route('/content')
def content():
    c = request.cookies.get('session cookie')
    if(c !='XXXXXCookieSetAfterUserLoginXXXXX'):
        return redirect('/login')
    else:
        return '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Login</title>
  </head>
  <body>
    <h1>Welcome! You have logged in!</h1>
    <a href='/sensitiveContent'>href to sensitive webpage</a>
  </body>
</html>
    '''
#page 3, sensitive content
@app.route('/sensitiveContent')
def sensitiveContent():
    c = request.cookies.get('session cookie')
    if(c !='XXXXXCookieSetAfterUserLoginXXXXX'):
        return redirect('/login')
    else:
        return '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Login</title>
  </head>
  <body>
    <h1>Welcome! Here is sensitive content page.</h1>
  </body>
</html>
    '''



#vulDemo is vulnerable to XSS, which when injecting cookie stealing js, can lead to cookie exfiltration.
#following set cookies to VulDemo.html page, to test cookie exfiltration.
@app.route('/vulDemo.html', methods=['GET'])
def vulDemo():
    response = make_response(send_file('vulDemo.html', mimetype='text/html'))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, ssl_context=(cert,key))
