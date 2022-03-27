#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 18:28:13 2022

@author: ldd775
"""

import socket, sys, re, os
import params

def recBytes():
    sys.path.append("../lib")       # for params
    

    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )



    progname = "echoserver"
    paramMap = params.parseParams(switchesVarDefaults)

    listenPort = paramMap['listenPort']
    listenAddr = ''       # Symbolic name meaning all available interfaces
    
    if paramMap['usage']:
        params.usage()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listenAddr, listenPort))
    s.listen(1)              # allow only one outstanding request
    # s is a factory for connected sockets

    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    archive = os.open("ArchivedFileByServer.txt",os.O_CREAT | os.O_RDWR)
    while 1:
        data = conn.recv(100)
        print("RECEIVING:")
        print(data)
        os.write(archive,data)
        if len(data) == 0:
            print("Zero length read, finished getting archive")
            break
        
def recBytes2():
    sys.path.append("../lib")       # for params
    

    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )



    progname = "echoserver"
    paramMap = params.parseParams(switchesVarDefaults)

    listenPort = paramMap['listenPort']
    listenAddr = ''       # Symbolic name meaning all available interfaces
    
    if paramMap['usage']:
        params.usage()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listenAddr, listenPort))
    s.listen(1)              # allow only one outstanding request
    # s is a factory for connected sockets
    while 1:
        conn, addr = s.accept()  # wait until incoming connection request (and accept it)
        rc = os.fork()
        if rc < 0:
            print("fork failed")
        elif rc == 0:
            print("child will execute")
            print('Connected by', addr)
            archive = os.open("ArchivedFileByServer.txt",os.O_CREAT | os.O_RDWR)
            while 1:
                data = conn.recv(100)
                print("RECEIVING:")
                print(data)
                os.write(archive,data)
                if len(data) == 0:
                    print("Zero length read, finished getting archive")
                    break
            unarchiver2()
            sys.exit(1)
        else:
            os.wait()
            continue

def unarchiver():
    archive = os.open("ArchivedFileByServer.txt", os.O_RDONLY)
    os.mkdir("UnArchivedFile")
    os.chdir("UnArchivedFile")
    header = os.read(archive,4)
    header = bytes(header)
    firstFileTitle = (os.read(archive,header[1])).decode()
    firstFile = os.open(firstFileTitle, os.O_CREAT | os.O_RDWR)
    os.write(firstFile, os.read(archive,header[3]))
    os.close(firstFile)
    while type(header) != None:
        try:
            header = os.read(archive,4)
            header = bytes(header)
        except:
            header = None
            continue
        if len(header) == 0:
            break
        nextFileTitle = (os.read(archive,header[1])).decode()
        nextFile = os.open(nextFileTitle, os.O_CREAT | os.O_RDWR)
        os.write(nextFile, os.read(archive,header[3]))
        os.close(nextFile)
    
    os.close(archive)
    
def unarchiver2():
    archive = os.open("/home/ldd775/os-project3-framing-lddavila/lib/ArchivedFileByServer.txt", os.O_RDONLY)
    
    directoryUserWantsToMake = input("Please enter the name of the file you want to unarchive into.")
    os.mkdir(directoryUserWantsToMake)
    os.chdir(directoryUserWantsToMake)
    
    header = os.read(archive,4)
    header = bytes(header)
    
    while(type(header) != None):
        # print("Value of the header",header)
        # print("Value of header[3]", header[3])
        # print("Class of header[3]",type(header[3]))
        
        if len(header) == 0:
            break
        fileBeingRestoredTitle = (os.read(archive,header[1])).decode()
        fileBeingRestored = os.open(fileBeingRestoredTitle, os.O_CREAT | os.O_RDWR)
        # print("Class of fileBeingRestored", type(fileBeingRestored))
        # print("Class of archive", type(archive))
        os.write(fileBeingRestored,os.read(archive,header[3]))
        try:
            header = os.read(archive,4)
            header = bytes(header)
        except:
            header = None
            continue
        print("Value of header",header)
        print("length of header",len(header))
        if len(header) == 0:
            break
        while (header[1] == 0):
            os.write(fileBeingRestored,os.read(archive,header[3]))
            header = os.read(archive,4)
            header = bytes(header)

        os.close(fileBeingRestored)
            
        
if __name__ == "__main__":
    recBytes2()
    #unarchiver2()