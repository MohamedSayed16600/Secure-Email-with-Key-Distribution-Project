import socket, threading
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

class ClientThread(threading.Thread):

    masterKeys={"18P7423@eng.asu.edu.eg": "cd30e2acb93ba4fc97e836c8ad01c324",
                     "18P7713@eng.asu.edu.eg":"000cf325452802fc12f9434ba8c93afb",
                     "18P5662@eng.asu.edu.eg":"d310b94fbb61e35821795d1f86b2305c",
                     "18p7423@eng.asu.edu.eg": "cd30e2acb93ba4fc97e836c8ad01c324",
                     "18p7713@eng.asu.edu.eg":"000cf325452802fc12f9434ba8c93afb",
                     "18p5662@eng.asu.edu.eg":"d310b94fbb61e35821795d1f86b2305c"
                     }
    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for ",ip,":",str(port))

    def run(self):
        print ("Connection from : ",ip,":",str(port))
        clientsock.send("Welcome to the multi-thraeded server".encode())
        data = "dummydata"
        infoCounter=0
        while len(data):
            if infoCounter==0:
                userEmail = self.csocket.recv(2048).decode()
                secretKey = self.generateSecret()
                userKey = self.getKey(userEmail)
                ciphertext = self.encrypt_message( userKey.encode(),secretKey)
                self.csocket.send(ciphertext)
                print("Client Secret Key Sent:",ciphertext)
                infoCounter+=1
            elif infoCounter==1:
                recepientEmail = self.csocket.recv(2048).decode()
                recepientKey =self.getKey(recepientEmail)
                ciphertext = self.encrypt_message(recepientKey.encode(),secretKey)
                self.csocket.send(ciphertext)
                print("Client Secret Key Sent:",ciphertext)
                infoCounter+=1
            elif infoCounter==2:
                self.csocket.close()
                print ("Client at ",self.ip," disconnected...")
                data=''
        

    def getKey(self,email):
        return self.masterKeys[email]
    
    def generateSecret(self):
        return get_random_bytes(16)
    
    def encrypt_message(self,key, message):
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(message)
        return ciphertext

host = "0.0.0.0"
port = 10000
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host,port))
while True:
    tcpsock.listen(4)
    print ("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.run()