import sqlite3

conn = sqlite3.connect(':memory:')

print( "opened database sucessfully")

conn.execute('''CREATE TABLE LOGINDATA
(USERNAME STRING PRIMARY KEY,
PASS STRING NOT NULL,
SALT STRING NOT NULL);''')

print( "table created successfully")

conn.execute("INSERT INTO LOGINDATA (USERNAME,PASS,SALT) \
	VALUES ('billy','password',10310)");

conn.commit()

print( "records created successfully")

cursor = conn.execute("SELECT USERNAME, PASS, SALT from LOGINDATA")
for row in cursor:
   print ("USERNAME = ", row[0])
   print ("PASS = ", row[1])
   print ("SALT = ", row[2])

print ("Operation done successfully")

conn.close()
