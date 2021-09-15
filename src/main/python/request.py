import requests
import json

def getEnviromentInfo(base_url):
    try:
        responseOld = requests.get(base_url + '/actuator/info', verify = False)
        responseNew = requests.get(base_url + '/api/actuator/info', verify = False)

        if(responseNew.status_code == 200):
            return getInfoFromResponse(responseNew)
        elif(responseOld.status_code == 200):
            return getInfoFromResponse(responseOld)
        else:
            return errorInfo()
    except Exception as e:
        return errorInfo()

def getInfoFromResponse(response):
    jsonData = response.json()

    author = jsonData["git"]["commit"]["user"]["name"]
    timestamp = jsonData["build"]["time"]
    sourceBranch = jsonData["git"]["branch"]
    jenkinsNumber = "Jenkins Build#" + jsonData["git"]["build"]["number"]
    commitMessage = jsonData["git"]["commit"]["message"]["full"]
    commitMessage = ' '.join(commitMessage.strip().split('\n'))

    return {
        "author": author,
        "timestamp": timestamp,
        "sourceBranch": sourceBranch,
        "jenkinsNumber": jenkinsNumber,
        "commitMessage": commitMessage

    }

def errorInfo():
    err = "Not responding"
    return {
            "author": err,
            "timestamp": err,
            "sourceBranch": err,
            "jenkinsNumber": err,
            "commitMessage": err
            }