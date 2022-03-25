#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
def sendBytes():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )


    progname = "framedClient"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage  = paramMap["server"], paramMap["usage"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        try:
            print(" attempting to connect to %s" % repr(sa))
            s.connect(sa)
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
            break

    if s is None:
        print('could not open socket')
        sys.exit(1)

    archive = os.open("ArchivedFile.txt",os.O_RDONLY)
    
    outMessage = os.read(archive,100)
    while len(outMessage):
        print("sending '%s'" % outMessage.decode())
        bytesSent = s.send(outMessage)
        outMessage = os.read(archive,100)

    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    
    os.close(archive)
    # outMessage = "Hello world!"
    # while len(outMessage):
    #     print("sending '%s'" % outMessage)
    #     bytesSent = s.send(outMessage.encode())
    #     outMessage = outMessage[bytesSent:]

    s.shutdown(socket.SHUT_WR)      # no more output

    while 1:
        data = s.recv(1024).decode()
        print("Received '%s'" % data)
        if len(data) == 0:
            break
    print("Zero length read.  Closing")
    s.close()
    
def archiver():
    archive = os.open("ArchivedFile.txt",os.O_CREAT | os.O_RDWR)
    os.write(1,("Please enter the File you'd like to archive\n").encode())                         #print the prompt
    userInput = (os.read(0,100))                        #get the next 100 chars of input from user
    userInput = (userInput.decode()).replace("\n","")   #remove the "\n" char
    os.chdir(userInput) #go to the user specified directory
   # print("THis is the user input:",userInput)
    #print(os.listdir(os.curdir))
    for fd in os.listdir(os.curdir): #for each file in the current directory
        print("Currently archiving the following file: " + fd)
        fileToBeArchived = os.open(fd, os.O_RDONLY)
        dataToBeArchived = os.read(fileToBeArchived,100)
        lengthOfData = len(dataToBeArchived)
        #print("Before the first whie loop")
        while len(dataToBeArchived) != 0: #this while loop gets the lenght of the data
            dataToBeArchived = os.read(fileToBeArchived, 100)
            #print(len(dataToBeArchived))
            lengthOfData += len(dataToBeArchived)
        os.close(fileToBeArchived)
        #print("after the first while loop")
        
        fileToBeArchived = os.open(fd, os.O_RDONLY)
        
        outOfBandData = [0,len(fd),len(fd),lengthOfData] #string that has "beginningofTitle,EndOfTitle,BeginningOfData,EndOfData"
        #print(outOfBandData)
        outOfBandData = bytearray(outOfBandData)
        os.write(archive,outOfBandData +(fd).encode()) #writes the title of file and out of band data to archive
        dataToBeArchived = os.read(fileToBeArchived, 100)#reads  first 100 bytes ofdata from the file to be archived
        #print(type(dataToBeArchived))
        
        
        while len(dataToBeArchived) != 0:
            os.write(archive, bytearray(dataToBeArchived)) #writes the data to the archive
            #print(bytearray(dataToBeArchived))
            dataToBeArchived = os.read(fileToBeArchived,100) #gets the next 100 bytes of data
    os.close(archive)

if __name__ == "__main__":
    archiver()
    #os.chdir("/home/ldd775")
    sendBytes()