const express = require('express');
const bodyParser= require('body-parser');
const {MongoClient} = require('mongodb');
const keys = require('./config/keys');

const app = express();
const path = require('path');
app.use(bodyParser.urlencoded({extended:true}));
const uri = encodeURI(keys.mongoURI);
// // CORS FOR API CALL
// app.use(function(req, res, next) {
// 	res.header("Access-Control-Allow-Origin", "*");
// 	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
// 	next();
//   });

app.use(express.static(path.join(__dirname)));

app.get('/',(req,res)=> {
	res.sendFile(path.join(__dirname+'/main.html'));
});

const {PythonShell} =require('python-shell');
app.post("/upload",(req,res,next)=>{
    let options = {
        mode: 'text',
        args: [req.body.match]
    };
    PythonShell.run('./Cricket-Fantasy-main/main.py', options, function (err, result){
    	if(result!=null){
    		res.json({
             status:true,
             message:result.toString()
          })
    	}
    	if(err){
    		res.json({
    			status: false,
    			message: err.toString()
    		});
    	}
          
    });
});

app.post('/test',(req,res)=> {
	res.send('You sent the name "' + req.body.name + '".');
});

app.get('/update',(req,res)=> {
	res.sendFile(path.join(__dirname+'/test.html'));
});

app.get('/json', (req,res)=> {
	// res.sendFile(path.join(__dirname+'/Cricket-Fantasy-main/points/seasonPoints.json'));
	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("points");

		var col = dbo.collection('seasonpoints');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/A',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('A');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/B',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('B');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/C',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('C');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/D',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('D');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/F',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('F');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/G',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('G');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/H',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('H');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

app.get('/team/E',(req,res) => {

	MongoClient.connect(uri, function(err,db){
		if(err)
			throw err;
		var dbo = db.db("auction");

		var col = dbo.collection('E');

		col.find({}).toArray(function (err, result) {
			if (err) {
				res.send(err);
			} else {
				res.send(JSON.stringify(result));
			}
		});
		
		db.close();
	});
});

const PORT = process.env.PORT || 5001;

app.listen(PORT);