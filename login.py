import sqlite3

conn = sqlite3.connect(':memory:')

print( "opened database sucessfully")

conn.execute('''CREATE TABLE LOGINDATA
(USERNAME BLOB PRIMARY KEY,
PASS BLOB NOT NULL,
SALT BLOB NOT NULL);''')

print( "table created successfully")

conn.execute("INSERT INTO LOGINDATA (USERNAME,PASS,SALT) \
	VALUES ('billy','password',10310)");
conn.execute("INSERT INTO LOGINDATA (USERNAME,PASS,SALT) \
	VALUES ('tom','password2',103112310)");
conn.execute("INSERT INTO LOGINDATA (USERNAME,PASS,SALT) \
	VALUES ('fuckoff','password3',55123)");

conn.commit()

print( "records created successfully")

cursor = conn.execute("SELECT USERNAME, PASS, SALT from LOGINDATA")
for row in cursor:
   print ("USERNAME = ", row[0])
   print ("PASS = ", row[1])
   print ("SALT = ", row[2])

print ("Operation done successfully")

t_user = 'billy'

cursor = conn.execute("SELECT * from LOGINDATA WHERE USERNAME IS '"+t_user+"'")
for row in cursor:
   print ("USERNAME = ", row[0])
   print ("PASS = ", row[1])
   print ("SALT = ", row[2])
   
   
t_user = 'ralph'

cursor = conn.execute("SELECT * from LOGINDATA WHERE USERNAME IS '"+t_user+"'")
row = cursor.fetchone()
if row is not None:
   print ("USERNAME = ", row[0])
   print ("PASS = ", row[1])
   print ("SALT = ", row[2])
else:
  print("no user found")

print ("Operation done successfully")

conn.close()
