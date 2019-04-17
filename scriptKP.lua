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
