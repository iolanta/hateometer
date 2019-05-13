treat = require('treat')
json = require('json')

function get_comments(splash, article, comments)
	local response = splash:http_get("https://c.rambler.ru/api/app/126/widget/init/?appId=126&xid=" .. article)
        local all_com = json.decode(treat.as_string(response.body))
	if all_com["comments"] ~= nil then
  		for i = 1, #all_com["comments"] do
    			table.insert(comments, all_com["comments"][i]["text"])
    		end
	end
end

function main(splash, args)
    splash.images_enabled = false
		local url = "https://lenta.ru/search/v2/process?from=0&size=5&sort=".. args['sort']

		if args['title_only'] == '1' then
			url = url .. "&title_only=".. args["title_only"]
		end

		url = url .. "&domain=1&query=" .. args["query"]

    local response = splash:http_get(url)
    local comments = {}
    local articles = {}
    local search = json.decode(treat.as_string(response.body))

    local found = #search["matches"]
    for i = 1, found do
			articles[i]={}
			articles[i]["title"] = search["matches"][i]["title"]
			local url_art = search["matches"][i]["url"]
			articles[i]["url"] = url_art
			articles[i]["comments"]= {}
			get_comments(splash, url_art, articles[i]["comments"])
			articles[i]["comments"] = treat.as_array(articles[i]["comments"])
    end

    return {list_articles = treat.as_array(articles)}
end
