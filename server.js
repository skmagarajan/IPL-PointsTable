const express = require('express');
const bodyParser= require('body-parser');

const app = express();
const path = require('path');
app.use(bodyParser.urlencoded({extended:true}));

app.get('/',(req,res)=> {
	res.send({hi: "Hello"});
});

app.listen('5001', function(){
	console.log("App is runnning on PORT 5001");
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