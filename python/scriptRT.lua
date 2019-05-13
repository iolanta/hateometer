treat = require('treat')

function prepare(splash)
   find_comments_wrapper = splash:jsfunc([[
    function (){
    	var comments = document.getElementsByClassName("comments__wrapper")[0].firstChild;
	var url = comments.getAttribute('data-post-url');
	var id = comments.getAttribute('data-post-id');
	return {url: url, id: id};
    }]])
end

function get_content(url, id)
	local part1 = [[
	<html><head> </head> <body><div class="comments__wrapper">
<script src="https://launcher.spot.im/spot/sp_oSi8qg2j" data-spotim-module="spotim-launcher" data-post-url="]]
	local part2 = [[" data-post-id="]]
	local part3 = [[" ></script></div>
</body>
 </html>]]
	return part1 .. url .. part2 .. id .. part3
end

function get_comments(splash, article, comments)
   splash:go(article)
   print("looking for comments")
   local url_id = find_comments_wrapper()
   splash:set_content(get_content(url_id['url'], url_id['id']))
   splash:wait(2)
   
   local iframe = splash:select('iframe')
   splash:go(iframe.attributes['src'])

   local all_comments = splash:select_all('[data-spot-im-class="message-text"]')
   for _, com in ipairs(all_comments) do
        comments[#comments+1] = com.textContent
    end
end

function main(splash, args)
  splash.images_enabled = false
  prepare(splash)
  splash:go("https://russian.rt.com/search?q=" .. args["query"])
  local all_articles = splash:select_all(".link_color")
  local len = math.min(#all_articles, 5)
  
  local comments = {}
  for i = 1, len do
    get_comments(splash,"https://russian.rt.com" .. all_articles[i]:getAttribute('href'),comments)	
  end

  return{ comments = treat.as_array(comments) }
end
