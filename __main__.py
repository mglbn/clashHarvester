from sqlite3 import connect
import sys
import os
from dotenv import load_dotenv
import grequests
import time
import socket
from clashTag import PlayerTag
import json
import requests
from db import DB
import manager
import signal

class GracefulKiller:
    running = True
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.running = False


def dump(data):
    try:
        with open("data/"+data["tag"]+".json","w") as f:
            json.dump(data,f)
    except:
        pass

class NoPlayerException(Exception):
    pass

def notifyonfailure(message):
    print(message)
    body = {
            "chat_id": os.environ["CHATID"],
            "text" : message
    }
    sent = False
    tries = 0
    while not sent and tries < 10:
        try:
            response = requests.post("https://api.telegram.org/bot"+os.environ["TELEGRAM"]+"/sendMessage",json=body).json()
            sent = response["ok"]
        except Exception as e:
            tries+=1
            time.sleep(2)
    return sent


def getPlayerData(tags):
    if len(tags)==0:
        return list()
    
    requests = (grequests.get(url= os.environ["BASEURL"]+tag,
        headers= {"Accept": "application/json", "Authorization": "Bearer "+ os.environ["TOKEN"]}) for tag in tags)
    responses = grequests.map(requests)
    for i in range(len(tags)):
        responses[i] = (tags[i],responses[i])

    players = list()
    tagsToTryAgain = list()
    
    for tag,res in responses:
    
        if res.status_code==200:
            players.append(res.json())
        elif res.status_code==404:
            continue
        else:
            tagsToTryAgain.append(tag)
            
    return players + getPlayerData(tagsToTryAgain)


def main():

    killer = GracefulKiller()
    
    task = None
    DB.connect(os.environ["DBHOST"],os.environ["DBUSER"], os.environ["DBPASSWORD"], os.environ["DBNAME"])  
    try:
        while killer.running:
            lap = 0
            task = manager.getNewWorkload()
            no_batches = int(task.get("size") / task.get("batchsize"))

            basetag = PlayerTag(task.get("tag"))
            for i in range(no_batches):
                tags = list()
                for j in range(task.get("batchsize")):
                    tags.append(str(basetag.getNext()))
                data = getPlayerData(tags)
                if len(data) > 0:
                    DB.insert(data)

            manager.confirm(task.get("tag"))
            lap +=1
            if lap == 5:
                break
            
            
    except NoPlayerException:
        pass
    except Exception as e:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        notifyonfailure(ip+"\n"+str(e.with_traceback))
        raise e
    DB.close()
    return 0



if __name__=="__main__":
    load_dotenv()
    sys.exit(main())