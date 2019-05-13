import json
import sys
import urllib.parse
import requests
import pickle
import re

def getCommentsLenta(key_words, sort, title_only):
    scriptLenta = ''
    with open("python/scriptLenta.lua", 'r') as f:
        scriptLenta = f.read()

    query = urllib.parse.quote_plus(key_words)
    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptLenta,
    'query': query,
    'sort' : sort,
    'title_only': title_only,
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
        all_com = len(coms)

        if(all_com == 0):
            results.append({"title": article['title'], "url": article['url'], "all": all_com, "pos": 0, "neg": 0})
        else:
            decision_list = loaded_model.decision_function(coms)

            pos_com = 0
            neg_com = 0

            for num in decision_list:
                if(num < -0.15):
                    neg_com += 1
                if(num > 0.15):
                    pos_com += 1
            results.append({"title": article['title'], "url": article['url'], "all": all_com, "pos": pos_com, "neg": neg_com})

    print(json.dumps(results, indent=2, ensure_ascii=False), flush = True)

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print(json.dumbs({error: "no query"}))
    else:
        with open('python/model.bin', 'rb') as f:
            loaded_model = pickle.load(f)
            articles = getCommentsLenta(sys.argv[1], sys.argv[2], sys.argv[3])
            if(len(articles) != 0):
                toneComments(articles, loaded_model)
            else:
                print(json.dumps({}, indent=2, ensure_ascii=False), flush = True)
