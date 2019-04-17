import requests
import json
import os.path

scriptRT = """
treat = require('treat')

function prepare(splash)
   find_comments_wrapper = splash:jsfunc([[
    function (){
    	var comments = document.getElementsByClassName("comments")[0];
    	comments.firstChild.lastChild.remove();
    	comments.firstChild.lastChild.remove();
        comments.firstChild.firstChild.removeAttribute("async");
   		comments.firstChild.firstChild.removeAttribute("data-ready");
    	return comments.innerHTML;
    }]])
end

function scrape_comments(splash)
    local iframe = splash:select('iframe')
    splash:go(iframe.attributes['src'])

    local comments = splash:select_all('[data-spot-im-class="message-text"]')
    local text = {}
    for _, com in ipairs(comments) do
        text[#text+1] = com.textContent
    end

    return text
end

function main(splash, args)
  splash.images_enabled = false
  prepare(splash)

  splash:go(args["page"])
  local title = splash:select("title"):text()
  local all_comments_page = find_comments_wrapper()

  splash:set_content(all_comments_page)
  splash:wait(2)
  local text = scrape_comments(splash)

  return{ name = title, comments = treat.as_array(text) }
end
"""

scriptKP = """
treat = require('treat')

function scrape_comments(splash)
    script = splash:set_content([[
        <html><head><script>

        var result;
        var ready = false;
        function loadcomments(ArticleClass,id,windowID){
	       ready = false;
		   let link = `https://s1.stc.m.kpcdn.net/interactive/api/1/comments/get.js/${windowID}/?comments.direction=page&comments.target.class=${ArticleClass}&comments.target.id=${id}&comments.target.spot=0&comments.number=1&sub=1`
		   window[windowID] = function(data){
	           let cmts = data.meta.comments;
			   let text =[];
			   for(i = 0; i < cmts.length; ++i){
			      text.push(cmts[i].text);
			    }
			      result = text;
	        }
		    var script = document.createElement("script");
		    document.getElementsByTagName('head')[0].appendChild(script);
		    script.onload = function() {
				ready = true;
		     };
		    script.async = false;
		    script.src = link;
}

        </script>
        </head>
        <body>
        </body>
        </html>
    ]])

    str = [[loadcomments("]] .. splash.args["articleclass"] .. [[","]] .. splash.args["id"] .. [[","]] .. splash.args["windowID"] .. [[")]]
    splash:runjs(str)
    splash:wait(1)
  	local coms = splash:evaljs("result")
  	return coms
end

function main(splash, args)
    splash.images_enabled = false
    splash:go(args["page"])
    local title = splash:select("title"):text()

    return {name = title, comments = scrape_comments(splash)}
end
"""

scriptLenta = """
treat = require('treat')
json = require('json')

function main(splash, args)
    splash.images_enabled = false
    splash:go(args["page"])
    local title = splash:select("title"):text()

    local response = splash:http_get("https://c.rambler.ru/api/app/126/widget/init/?appId=126&xid=" .. args["page"])
    local all_com = json.decode(treat.as_string(response.body))["comments"]
  	local comments = {}
  	for i = 1, #all_com do
    	table.insert(comments, all_com[i]["text"])
    end

    return {name = title, comments = treat.as_array(comments)}
end

"""

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

def getCommentsRT(url):
    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptRT,
    'page': url,
    'timeout': 40
    })
    appendDataToJson(resp.json(), 'all_comments.json')


def getCommentsKP(url, id, articleClass):
    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptKP,
    'page': url,
    'timeout': 40,
    'articleclass': articleClass,
    'id': id,
    'windowID': 'a4fd37834'
    })

    appendDataToJson(resp.json(), 'all_comments.json')

def getCommentsLenta(url):
    resp = requests.get("http://0.0.0.0:8050/execute", params={
    'lua_source': scriptLenta,
    'page': url,
    'timeout': 40
    })

    #print(resp.json())
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

#getCommentsKP('https://www.kp.ru/daily/26956/4010007/', '4010007', '13')

#getCommentsRT('https://russian.rt.com/nopolitics/article/616066-kniga-kristina-potupchik-telegram')
#getCommentsRT('https://russian.rt.com/opinion/617412-prohanov-rossiya-tvorcy-mechtateli-gosudarstvo-vozrozhdenie')

#getCommentsLenta("https://lenta.ru/news/2019/04/12/zagitova_gymnastic/")


countCom()
