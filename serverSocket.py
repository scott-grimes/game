import socket, sysconfig
from thread import *

HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST,PORT))
except socket.error, msg:
    print 'FAILED to bind socket'
    sys.exit()
        
            
s.listen(10)
print 'socket is now listening'

def clientthread(conn,addr):
    #Sending message to connected client
    conn.sendall('Welcome to the server. Type your command and hit enter\nEscape Character is "^"') 
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)
        if(data == "^"):
            conn.sendall('Closing Connection...')
            conn.close()
            print "Connection closed at clients request: "+addr[0] + ':'+str(addr[1])
            return
        reply = 'OK...' + data
        if not data: 
            break
        print "sending: "+reply
        conn.sendall(reply)
        
    #came out of loop
    conn.close()

while True:
    conn, addr = s.accept()
    
    print +addr[0] + ':'+str(addr[1])+" has connected"
    
    start_new_thread(clientthread ,(conn,addr))
    
conn.close()
s.close()