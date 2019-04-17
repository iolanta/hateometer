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

function get_comments(splash, article, comments)
   splash:go(article)
   local all_comments_page = find_comments_wrapper()
   splash:set_content(all_comments_page)
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
