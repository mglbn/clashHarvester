import requests
import time
_mngnt_server_url= "http://91.200.100.224:17823"

def getNewWorkload():
    while True:
        try:
            resp = requests.get(_mngnt_server_url + "/workload")
            json = resp.json()
            return json
        except requests.JSONDecodeError:
            print("Managementserver offline. Versuche erneut in 20s.")
            time.sleep(20)
            continue

def confirm(oldtag):
    para = {"oldtag":oldtag}
    requests.get(_mngnt_server_url + "/confirmWorkload",params=para)