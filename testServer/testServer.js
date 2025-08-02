const express = require('express');
const http = require('http');
const app = express();
http.createServer(app).listen(80, () => {
    console.log('HTTP server is running');
  });
  app.get('/api/system/ping', (req, res) => {
    res.send('ok');
  });