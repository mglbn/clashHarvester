import requests
from dotenv import load_dotenv
import os

load_dotenv()
_mngnt_server_url= os.environ["MANAGER"]

def getNewWorkload(oldtag=None):
    if oldtag == None:
        resp = requests.get(_mngnt_server_url + "/workload")
    else:
        para = {"oldTag": oldtag}
        resp = requests.get(_mngnt_server_url + "/workload",params=para)
    json = resp.json()
    return json
        