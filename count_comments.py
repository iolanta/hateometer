import json
import sys
import urllib.parse
import requests
import pickle
import re

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

    if(not resp.json()):
        return []
    return resp.json()

def new_preprocessor(str):
    str = str.lower()
    str = re.sub("(\\s+!+)", "!", str)
    str = re.sub("(\s+\(+)", "(", str)
    str = re.sub("(\s+\)+)", ")", str)
    return str

def toneComments(articles, model):
    results = []
    for article in articles['list_articles']:
        coms = article['comments']

        if(len(coms) == 0):
            results.append({"title": article['title'], "pos": 0, "neg": 0})
        else:
            decision_list = loaded_model.decision_function(coms)

            pos_com = 0
            neg_com = 0

            for num in decision_list:
                if(num < -0.18):
                    neg_com += 1
                if(num > 0.18):
                    pos_com += 1
            results.append({"title": article['title'], "pos": pos_com, "neg": neg_com})

    print(json.dumps(results, indent=2, ensure_ascii=False), flush = True)

if __name__ == '__main__':
    if(sys.argv[1] == "test"):
        print(json.dumps({"title": 'test', "pos": 10, "neg": 5}, indent=2, ensure_ascii=False), flush = True)
    else:
        with open('model.bin', 'rb') as f:
            loaded_model = pickle.load(f)

        articles = getCommentsLenta(sys.argv[1])
        if(len(articles) != 0):
            toneComments(articles, loaded_model)
        else:
            print(json.dumps({"title": 'None', "pos": 0, "neg": 0}, indent=2, ensure_ascii=False), flush = True)
