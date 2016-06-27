import socket
import sys
import pdb
import threading
import httplib
import time
import os
import requests

#Creating a socket port number variable
serverPortNumber = int(8080) # Takes the port number as 8080
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket is a function that creates a socket

# Binding and Listening using Socket
print "Server starting..."
serverSocket.bind(('127.0.0.1', serverPortNumber))
serverSocket.listen(300)
threads =[];
time1=0
i=0
os.getcwd();
os.mkdir("Cache")

class ThreadProxy(threading.Thread):
    # Used to assign a particular thread variable to its object
    def __init__(self,partitionedMessage, clientSocket):
        threading.Thread.__init__(self)
        self.partitionedMessage = partitionedMessage
        self.clientSocket = clientSocket
    def run(self):
        
    #Caching a Request
        # Getting the requestType and URL from the message received from User
        requestType = self.partitionedMessage[0]
        requestAddress = self.partitionedMessage[1]
        requestAddress = requestAddress[1:]
        print "Request is ", requestType, " to URL : ", requestAddress
        
    #Searching if the Request is available in the Cache
        searchFile = os.getcwd()+"\Cache"
        searchFile = searchFile+"\\"+requestAddress
        try:
            # Opening the file if it is present
            file = open(searchFile[0:], "r")
            searchFileResult = file.readlines()
            print "The file already exists in the cache of proxy server\n\n"

        #If the file is present then Proxy will send the Data
            for f in range(0, len(searchFileResult)):
                print (searchFileResult[f])
                self.clientSocket.send(searchFileResult[f])
            print "Started reading file from cache\n"
            # Calculating the time end time of processing the User Request
            time2 = int(round(time.time()*1000));
            # Opening the Log file
            fo = open(os.getcwd()+"/Cache/log.txt","a")
            # Calculating the Round Trip Time for the whole Request and writing it to the log file
            fo.write("Round Trip Time: "+str(time2-time1)+"\n"+"\n"+"\n"+"\n")
            fo.close()

        # When the file is not there in the cache and exception is generated
        except IOError:
                print "File is not there in the cache\n taking file from the original server\n creating cache in the proxy server"
                # Connecting the Proxy Server to HTTP port 80 to get the Client Object from the Original Server
                proxyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # Connecting the proxy to port 80 with the requested Address
                    proxyServer.connect((requestAddress, 80))
                    print 'Socket successfully connected to the port 80 of the host'
                    proxyNewFile = proxyServer.makefile('r', 0)
                    # Putting the GET Request to the Server
                    proxyNewFile.write("GET / HTTP/1.0\r\nHost: "+requestAddress+"\r\n\r\n")
                    
                    
                                

            # Take a temporary variable and record data in it
                    buffer = proxyNewFile.readlines()
            # Raising an Exception if the errors are 400 and 405"
                    if "400" in buffer[0]:
                        raise ValueError('400 Bad Request')
                    elif "405" in buffer[0]:
                        raise ValueError('405 Method Not Allowed')
                   
                
            # Create a file for the new request in the cache, Send the response to the client socket
                    bufferFile = open(os.getcwd()+"\Cache\./" + requestAddress, "wb")
                    for i in range(0, len(buffer)):
                        bufferFile.write(buffer[i])
                        self.clientSocket.send(buffer[i])

                    # Calculating the end time when the object is brought from the original Server
                    time2 = int(round(time.time()*1000));
                    fo = open(os.getcwd()+"\Cache\log.txt","a")
                    # Calculating the Round Trip Time and logging it in the Log File
                    fo.write("Round Trip Time: "+str(time2-time1)+"\n"+"\n"+"\n"+"\n")
                    fo.close()
                except socket.gaierror:
                    print 'Illegal Request'
                    self.clientSocket.close()
                # Handling 404 Page not found error
                except Exception as error:
                    print error
                # Handling any other Exception
               
            
                
    
while True:
    # Start receiving data from the client
    print 'Starting the server \nReady to Serve\n'
    if i==0:
        # Calculating the beginning time of Request
        time1 = int(round(time.time()*1000))
    try:
        # Accept a connection from client
        clientSocket, address = serverSocket.accept() 
    except Exception:
        print "Cannot connect"
        
    print ' connection received from: ', address
    #Recieves data from Socket
    message = clientSocket.recv(1024)
    
    partitionedMessage = message.split()

    if len(partitionedMessage) <= 1:
        continue
    mi = partitionedMessage[1]
    try:
        # Getting Content-Length(Response-Length) from the Data Received
        head1 = requests.head("http://"+mi[1:])
        headers1 = head1.headers
        messageLength = str(len(message))
        contentLength = headers1['Content-Length']
        # Creating Log file 
        fo = open(os.getcwd()+"/Cache/log.txt","a")
        fo.write("Host Address: "+ socket.gethostbyname(str(mi[1:])))
        fo.write("\nHost Name: "+str(mi[1:])+"\n")
        fo.write("Local Port: 8080\n")
        fo.write("Request Length: "+messageLength+"\n")
        fo.write("Response Length: "+ contentLength+"\n")
        fo.write("\n\n\n"+message)
        fo.close();
    # Handling Get Address Info Exception
    except Exception as error:
        print ''

    # Creating thread for each request (Multithreading)
    thread = ThreadProxy(partitionedMessage, clientSocket)
    thread.start()
    threads.append(thread)
    # Joining the Threads (Multithreading)
    for singleThread in threads:
        singleThread.join()
