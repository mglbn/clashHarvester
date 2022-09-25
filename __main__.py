import sys
import os
from urllib.error import HTTPError
from dotenv import load_dotenv
import requests
import time
import socket


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


def getPlayerData(tag):
    response = requests.get(url= os.environ["BASEURL"]+tag,
        headers= {"Accept": "application/json", "Authorization": "Bearer "+ os.environ["TOKEN"]})
    if not response.status_code==200:
        raise HTTPError(response)

    body= response.json()

    if body.get("reason")=="notFound":
        raise NoPlayerException("")
    
    if body.get("tag")== None:
        raise Exception("smth wrong with body")

    return body


def main():
    try:
        print(getPlayerData("Y8YGQLJ0"))
    except NoPlayerException:
        pass
    except Exception as e:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        notifyonfailure(ip+"\n"+str(e.with_traceback))
    return 0

if __name__=="__main__":
    load_dotenv()
    sys.exit(main())