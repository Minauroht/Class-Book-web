const express = require('express');
const { list } = require('mongodb/lib/gridfs/grid_store');
const app = express()
app.use(express.urlencoded({ extended: true }));
const MongoClient = require('mongodb').MongoClient
app.set('view engine', 'ejs')
const methodOverride = require('method-override')
app.use(methodOverride('_method'))


// db연결
var db;
MongoClient.connect('mongodb+srv://jiwooseol:twin0413@cluster0.dl5s8dn.mongodb.net/booknight?retryWrites=true&w=majority', { useUnifiedTopology: true }, function(error, client){
  if (error) return console.log(error)

  db = client.db('booknight');

  app.listen(8080, function() {
    console.log('listening on 8080')
  })
})

// index.html
app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html')
})

// booking.html 주소
app.get('/booking', function(req, res){
    res.sendFile(__dirname + '/booking.html')
})

// booking.html 주소
app.get('/checking', function(req, res){
    res.sendFile(__dirname + '/checking.html')
})