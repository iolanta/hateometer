import requests
import json
import os.path
import urllib.parse

def appendDataToJson(json_data, file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as fw:
            fw.write(json.dumps([json_data], indent=2, ensure_ascii=False))

    else:
        old_json_data = []
        with open(file_path, 'r') as fr:
            old_json_data = json.loads(fr.read())
            fr.close()

        old_json_data.append(json_data)
        with open(file_path, 'w') as fw:
            fw.write(json.dumps(old_json_data, indent=2, ensure_ascii=False))

def getCommentsRT(key_words):
    scriptRT = ''
    with open("scriptRT.lua", 'r') as f:
        scriptRT = f.read()

    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptRT,
    'query': "war",
    'timeout': 40
    })
    appendDataToJson(resp.json(), 'all_comments.json')


def getCommentsKP(url, id, articleClass):
    scriptKP = ''
    with open("scriptKP.lua", 'r') as f:
        scriptKP = f.read()

    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptKP,
    'page': url,
    'timeout': 40,
    'articleclass': articleClass,
    'id': id,
    'windowID': 'a4fd37834'
    })

    appendDataToJson(resp.json(), 'all_comments.json')

def getCommentsLenta(key_words):
    scriptLenta = ''
    with open("scriptLenta_old.lua", 'r') as f:
        scriptLenta_old = f.read()
    query = urllib.parse.urlencode({"query": key_words})
    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptLenta_old,
    'query': query,
    'timeout': 40
    })
    appendDataToJson(resp.json(), 'all_comments.json')

def countCom():
    pos_comments = []
    neg_comments = []
    neutral_comments = []

    with open("pos_comments.json", 'r') as fp:
        pos_comments = json.loads(fp.read())
        print(len(pos_comments))
    with open("neg_comments.json", 'r') as fn:
        neg_comments = json.loads(fn.read())
        print(len(neg_comments))
    with open("neutral_comments.json", 'r') as fn:
        neutral_comments = json.loads(fn.read())
        print(len(neutral_comments))

if __name__ == '__main__':
    #getCommentsKP('https://www.kp.ru/daily/26981/4040796/', '4040796', '13')

    #getCommentsLenta("тюрьма за репосты")

    countCom()
