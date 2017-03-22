import os, hashlib, sqlite3, binascii

db = sqlite3.connect('logins.db')

db.execute('''CREATE TABLE IF NOT EXISTS LOGINDATA 
    (USERNAME BLOB PRIMARY KEY,
PASS BLOB NOT NULL,
SALT BLOB NOT NULL);''')

def print_all_users():
    cursor = db.execute("SELECT * from LOGINDATA")
    for row in cursor:
       print("USER = "+ row[0])
       print ("PASS = "+ row[1])
       print ("SALT = "+ row[2])
       print("")

def user_is_in_database(name):
    cursor = db.execute("SELECT * from LOGINDATA WHERE USERNAME IS ?",(name,))
    row = cursor.fetchone()
    return (row is not None)

def add_user_serverSide(input):
    name = input[0]
    password = input[1]
    salt = input[2]
    
    if (not user_is_in_database(name)):
        db.execute("INSERT INTO LOGINDATA (USERNAME,PASS,SALT) \
    VALUES (?,?,?);",(name,password,salt))
        db.commit()
        return True
    
    return False

def checkPass(name, password):
    cursor = db.execute("SELECT * from LOGINDATA WHERE USERNAME IS ?",(name,))
    row = cursor.fetchone()
    if row is not None:
        hashed = hashlib.pbkdf2_hmac('sha256',password,binascii.unhexlify(row[2]),100000)
        print "entered"+binascii.hexlify(hashed)
        print "actual"+row[1]
        if row[1] == binascii.hexlify(hashed):
            return True
    return False

def changePass_server_side(name, password, newPassword):
    if(checkPass(name,password)):
        
        salt = os.urandom(16)
        password = newPassword.encode()
    
        hashed_pass = hashlib.pbkdf2_hmac('sha256',password,salt,100000)
        hashed_pass = binascii.hexlify(hashed_pass)
        salt = binascii.hexlify(salt)
        db.execute("""UPDATE LOGINDATA     
            SET PASS = ?,    
                SALT = ?
            WHERE USERNAME = ?;""",(hashed_pass,salt,name,))
        db.commit()
        return True
        
    return False

def add_user_clientSide(name, password):
    salt = os.urandom(16)
    password = password.encode()
    
    hashed_pass = hashlib.pbkdf2_hmac('sha256',password,salt,100000)
    hashed_pass = binascii.hexlify(hashed_pass)
    salt = binascii.hexlify(salt)
    
    output = [name,hashed_pass,salt]
    return add_user_serverSide(output)




choice = raw_input("Login : 1\n New User : 2\n Change Pass : 3 \n Print Users :4 ")
if(choice == "1"):
    print "Login Now:"
    uName = raw_input("Username: ")
    uPass = raw_input("Password: ")
    if(checkPass(uName,uPass)):
        print "Sucess"
    else:
        print "Incorrect Username or Password"

elif(choice=="2"):
    uName = raw_input("Username: ")
    uPass = raw_input("Password: ")
    if add_user_clientSide(uName,uPass):
        print "Sucessfully added uName!"
    else:
        print "Username Taken!"
elif(choice=="3"):
    uName = raw_input("Username: ")
    uPass = raw_input("Current Password: ")
    uNewPass = raw_input("New Password: ")
    if changePass_server_side(uName,uPass,uNewPass):
        print "Sucessfully changed Password!"
    else:
        print "Your Username or Original Password is incorrect! Your password was not updated!"
elif(choice=="4"):
    print_all_users()
else:
    print "invalid selection!"

