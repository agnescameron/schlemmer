var express = require('express')
var http = require('http');
var fs = require('fs');
const utf8 = require('utf8');
var ws = require('ws')
 
var app = express();
 
// parse urlencoded request bodies into req.body
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended: false}));
 

app.use(express.static('public'));

// respond to all requests
app.get('/', function(req, res){
	console.log('get request')
	res.send('ooo')
});
 

var WebSocketServer = require('ws').Server,
wss1 = new WebSocketServer({port: 40510})
wss2 = new WebSocketServer({port: 40511})


wss1.on('connection', function (ws) {
	wss1.clients.forEach(function(client){
	  ws.on('message', function (message) {
	    console.log('received: %s', message)
	  })
	  setInterval(
	    () => { 
		  fs.readFile('./data1.txt', function(err, data) {
			   	try{
			    	ws.send(`${data}`)
			   	}
			    catch(err){
			    	// console.log('sorry babe')
			    }
			});
		  });
	   }, 100)
})

wss2.on('connection', function (ws) {
	wss2.clients.forEach(function(client){
	  ws.on('message', function (message) {
	    console.log('received: %s', message)
	  })
	  setInterval(
	    () => { 
		  fs.readFile('./data2.txt', function(err, data) {
			   	try{
			    	ws.send(`${data}`)
			   	}
			    catch(err){
			    	// console.log('sorry babe')
			    }
			});
		  });
	   }, 100)
})


var server = app.listen(8080, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://%s:%s", host, port)
})

