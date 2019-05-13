var express = require('express');
const pug = require('pug');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Hate-o-meter' });
});

router.get('/api', function(req,res,next){
  let q = req.query.q;
  let sort = req.query.s;
  let title_only =  req.query.t;
  const spawn = require("child_process").spawn;
  console.log("got query:"+q);
  const pythonProcess = spawn('python3',["python/count_comments.py", q, sort, title_only]);
  pythonProcess.stdout.on('data', (data) => {
    data = JSON.parse(data)
    var html = pug.renderFile("./views/articles.pug",{
       result: data,
       query: q,
       cache: false,
       doctype: "html",
       compileDebug: true
    })
    res.write(html);
    res.end();
  });
  res.type('html');
  res.status(200);
});

module.exports = router;
