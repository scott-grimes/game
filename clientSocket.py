import socket, sys

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error, msg:
    print "failure. Error code: " + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

host = 'localhost'
port = 8888

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
    
s.connect((remote_ip,port))
#print "socket connected to "+host+ " on "+ remote_ip



while True:
    reply = s.recv(4096)
    if(reply == "Closing Connection..."):
        print "Connection Closed"
        break
    
    if not reply: 
            break
    #Now receive data
    print reply
        
        
    message = raw_input("command: ")
    
    try:
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed \n '+socket.error
    

s.close()