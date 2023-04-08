import sqlite3
import os
import argparse

def create_connection (DIR,db_file):
        conn = None
        try:
            conn = sqlite3.connect(os.path.join(DIR,db_file)) #create db_file if doesn't exist
            print('[+db]  connect successed!')
            return conn
        except OSError as e:
            print(e)
            return None

#initiate 3 datatables: content, credential, cookie
def create_db(conn):
    try:
        conn.execute('CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY AUTOINCREMENT , location TEXT NOT NULL, content BLOB)')
        conn.execute('CREATE TABLE IF NOT EXISTS credential (id INTEGER PRIMARY KEY AUTOINCREMENT , username TEXT NOT NULL, password TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS cookie (id INTEGER PRIMARY KEY AUTOINCREMENT , location TEXT NOT NULL, cookie TEXT)')   
    except OSError as e:
        print(e)    

#content I and L(location), and G(find content per location)
def insert_content(conn,location,content):
    try:
        conn.execute("INSERT INTO content (location, content) VALUES (?, ?)", (location, content))
        rowid = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        print(f'\033[1;32m[+db] Content inserted successed! @row {rowid}\033[0m')
    except OSError as e:
        print(e)

def list_Content(conn):
    try:
        cursor = conn.execute("SELECT location, content FROM content")
        found = cursor.fetchall()
        for element in found:
            print(f'url:content -> {element[0]}:{element[1]}')
    except OSError as e:
        print(e)


def list_location(conn):
    try:
        cursor = conn.execute("SELECT location FROM content")
        found = cursor.fetchall()
        for element in found:
            print(element[0])
    except OSError as e:
        print(e)

def get_content(conn,location):
    try:
        cursor = conn.execute("SELECT content FROM content WHERE location = ?", (location,))
        found = cursor.fetchone()[0]
        print(found)
    except OSError as e:
        print(e)



#credential I and List
def insert_credential(conn,username,password):
    try:
        conn.execute("INSERT INTO credential (username, password) VALUES (?, ?)", (username, password))
        rowid = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        print(f'\033[1;32m[+db] Credential inserted successed! @row {rowid}\033[0m')
    except OSError as e:
        print(e)

def list_credential(conn):
    try:
        cursor = conn.execute("SELECT username,password FROM credential")
        found = cursor.fetchall()
        for element in found:
            print(f'username:password -> {element[0]}:{element[1]}')
    except OSError as e:
        print(e)

#cookie I and List
def insert_cookie(conn,location,cookie):
    try:
        conn.execute("INSERT INTO cookie (location, cookie) VALUES (?, ?)", (location, cookie))
        rowid = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        print(f'\033[1;32m[+db] Cookies inserted successed! @row {rowid}\033[0m')
    except OSError as e:
        print(e)

def list_cookie(conn):
    try:
        cursor = conn.execute("SELECT location, cookie FROM cookie")
        found = cursor.fetchall()
        for element in found:
            print(f'location:cookie -> {element[0]}:{element[1]}')
    except OSError as e:
        print(e)


def main():
    DIR = r"." #To change according to your env.
    database = r"sqlite.db"
    parser = argparse.ArgumentParser()

    #DB founctional
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create', '-C', action='store_true', help='Create Database')
    group.add_argument('--insert','-I', action='store_true', help='Insert')

    group.add_argument('--listContent','-Lc', action='store_true', help='List all content')
    group.add_argument('--listLocation','-Ll', action='store_true', help='List all locations in content table')
    group.add_argument('--getContent','-G', action='store_true', help='Get content when providing location')
    
    group.add_argument('--listCookie','-Lk', action='store_true', help='List all cookies')
    
    group.add_argument('--listCredential','-Lp', action='store_true', help='List all credentials')

    #exfiltrate credential (p)
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    
    #exfiltrate page content (c)
    parser.add_argument('--location', '-l')
    parser.add_argument('--content', '-c')

    #exfiltrate cookie (k)
   # parser.add_argument('--location', '-l')
    parser.add_argument('--cookie', '-k')

    args = parser.parse_args()

    conn = create_connection(DIR,database)

    if(args.create):
        print("[+] Initiating database")
        create_db(conn)
    
    elif(args.insert): #insert to one datatable at one time
        if(args.location is not None and args.content is not None):
            print("[+] Inserting content")
            insert_content(conn, args.location, args.content)            
        elif(args.location is not None and args.cookie is not None):
            print("[+] Inserting cookie")
            insert_cookie(conn, args.location, args.cookie)
        elif(args.username is not None and args.password is not None):
            print("[+] Inserting credential")
            insert_credential(conn, args.username, args.password)
        else:
            parser.error("--insert requires --location and --content ||OR --location and --cookie ||OR --username and --password ")

    elif(args.listContent):
        print("[+db] Listing all content in content table")
        list_Content(conn)

    elif(args.listLocation):
        print("[+db] Listing all locations in content table")
        list_location(conn)
 
    elif(args.getContent):
        if(args.location is None):
            parser.error("--getContent requires --location")
        else:
            print("[+db] Getting content with given url")
            get_content(conn, args.location)
    
    elif(args.listCookie):
        print("[+db] Listing all exfiltrated cookies")
        list_cookie(conn)
    
    elif(args.listCredential):
        print("[+db] Listing all exfiltrated credentials")
        list_credential(conn)

if __name__ == "__main__":
    main()
