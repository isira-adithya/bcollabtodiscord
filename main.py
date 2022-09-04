import requests
import json
import base64
import time

# Variables
shouldStop = False

# Reading the settings.json file
try:
    _settings = json.load(open('settings.json', 'r'))
except Exception as e:
    print("[ERR] Cannot read the 'settings.json' file.")
    pass

# Template Generators
def getHTTPMessageFromTemplate(cResponse):
    templateString = ""
    with open('./templates/http.txt', 'r') as wF:
        templateString = templateString = wF.read()
        templateString = templateString.replace("{{type}}", "HTTP")
        templateString = templateString.replace("{{protocol}}", cResponse['protocol'])
        templateString = templateString.replace("{{from}}", cResponse['client'])
        templateString = templateString.replace("{{time}}", cResponse['time'])
        templateString = templateString.replace("{{request}}", base64.b64decode(cResponse['data']['request']).decode('utf-8'))
        templateString = templateString.replace("{{response}}", base64.b64decode(cResponse['data']['response']).decode('utf-8'))
    return templateString

def getDNSMessageFromTemplate(cResponse):
    templateString = ""
    with open('./templates/dns.txt', 'r') as wF:
        templateString = wF.read()
        templateString = templateString.replace("{{type}}", "DNS")
        templateString = templateString.replace("{{from}}", cResponse['client'])
        templateString = templateString.replace("{{domain}}", cResponse['data']['subDomain'])
        templateString = templateString.replace("{{time}}", cResponse['time'])
        try:
            templateString = templateString.replace("{{request}}", base64.b64decode(cResponse['data']['rawRequest']).decode('utf-8'))
        except Exception as e:
            templateString = templateString.replace("{{request}}", cResponse['data']['rawRequest'])
    return templateString

def getSMTPMessageFromTemplate(cResponse):
    templateString = ""
    with open('./templates/smtp.txt', 'r') as wF:
        templateString = wF.read()
        templateString = templateString.replace("{{type}}", "SMTP")
        templateString = templateString.replace("{{sender}}", cResponse['data']['sender'])
        templateString = templateString.replace("{{time}}", cResponse['time'])
        templateString = templateString.replace("{{recipients}}", base64.b64decode(cResponse['data']['recipients']).decode('utf-8'))
        templateString = templateString.replace("{{message}}", base64.b64decode(cResponse['data']['message']).decode('utf-8'))
        templateString = templateString.replace("{{conversation}}", base64.b64decode(cResponse['data']['conversation']).decode('utf-8'))
    return templateString

# Discord Message Sender
def sendToDiscord(message):
    data = {
        "content" : message,
        "username" : "bcollabtodiscord"
    }
    requests.post(_settings['dWebhook'], json=data)
    

# Checking if the given information is correct
res = requests.post(f"https://{_settings['cdomain']}/bcollabtodiscord/test", json={"time":time.localtime()})
if (res.status_code == 200):
    resContent = res.content.decode()
    res = requests.get(f"{_settings['polling-endpoint']}?biid={_settings['biid']}")
    if (res.status_code == 200):
        cResults = json.loads(res.content.decode())
        for cResponse in cResults['responses']:
            if (cResponse['protocol'] == 'https' or cResponse['protocol'] == 'http'):
                message = getHTTPMessageFromTemplate(cResponse)
            elif (cResponse['protocol'] == 'dns'):
                message = getDNSMessageFromTemplate(cResponse)
            elif (cResponse['protocol'] == 'smtp'):
                message = getSMTPMessageFromTemplate(cResponse)
            else:
                message = json.dumps(cResponse)
            sendToDiscord(message=message)

# Main polling loop
while (not shouldStop):
    try:
        res = requests.get(f"{_settings['polling-endpoint']}?biid={_settings['biid']}")
        if (res.content.decode() == r"{}"):
            time.sleep(3)
            continue
        print(f"[LOG] Found {len(cResults['responses'])} Interactions.")
        if (res.status_code == 200):
            cResults = json.loads(res.content.decode())
            for cResponse in cResults['responses']:
                if (cResponse['protocol'] == 'https' or cResponse['protocol'] == 'http'):
                    message = getHTTPMessageFromTemplate(cResponse)
                elif (cResponse['protocol'] == 'dns'):
                    message = getDNSMessageFromTemplate(cResponse)
                elif (cResponse['protocol'] == 'smtp'):
                    message = getSMTPMessageFromTemplate(cResponse)
                else:
                    message = json.dumps(cResponse)
                sendToDiscord(message=message)
        time.sleep(3)
    except Exception as e:
        if ('KeyboardInterrupt' in str(e)):
            print("[LOG] Script Ended.")
        else:
            print("[ERR] Something went wrong.")
            print(e)