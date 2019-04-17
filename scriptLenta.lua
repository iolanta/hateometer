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
    local response = splash:http_get("https://lenta.ru/search/v2/process?from=0&size=1&sort=1&title_only=1&domain=1&" .. args["query"])

    local comments = {}
    local article = json.decode(treat.as_string(response.body))
    
    if article["matches"][1]["url"] ~= nil then
	get_comments(splash, article["matches"][1]["url"], comments)
    end

    return {comments = treat.as_array(comments)}
end
