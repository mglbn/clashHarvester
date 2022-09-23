import sys
import os
from urllib import response
from dotenv import load_dotenv
import requests

def getplayer(tag):
    response = requests.get(url= os.environ["BASEURL"]+tag,
    headers= {"Accept": "application/json", "Authorization": "Bearer "+ os.environ["TOKEN"]})

    #Do some error handling

    return response.json()


def main():
    print(getplayer("Y8YGQLJ0"))
    return 0


if __name__=="__main__":
    load_dotenv()
    sys.exit(main())
