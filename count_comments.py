import json
import sys
import urllib.parse
import requests
import pickle
from sklearn.svm import SVC

def getCommentsLenta(key_words):
    scriptLenta = ''
    with open("scriptLenta.lua", 'r') as f:
        scriptLenta = f.read()

    query = urllib.parse.quote_plus(key_words)

    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptLenta,
    'query': query,
    'timeout': 40
    })

    if(not resp.json()['comments']):
        return []
    return resp.json()['comments']

def toneComments(comments):
    with open('model.bin', 'rb') as f:
        loaded_model = pickle.load(f)
    decision_list = loaded_model.decision_function(comments)

    pos_com = 0
    neg_com = 0

    for num in decision_list:
        num = round(num, 2)
        if(num < -0.20):
            neg_com += 1
        if(num > 0.20):
            pos_com += 1

    print(json.dumps({"pos": pos_com, "neg": neg_com}, indent=2, ensure_ascii=False), flush = True)

if __name__ == '__main__':
    list_all_comments = getCommentsLenta(sys.argv[1])
    if(len(list_all_comments) != 0):
        toneComments(list_all_comments)
