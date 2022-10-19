import requests

_mngnt_server_url= "http://91.200.100.224:17823"

def getNewWorkload():
    
    resp = requests.get(_mngnt_server_url + "/workload")
    json = resp.json()
    return json

def confirm(oldtag):
    para = {"oldtag":oldtag}
    requests.get(_mngnt_server_url + "/confirmWorkload",params=para)