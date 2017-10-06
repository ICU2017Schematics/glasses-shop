var express = require('express');
var router = express.Router();
const MongoClient = require('mongodb').MongoClient

const dburl = 'mongodb://ibmuser:ibmpassword@ds053784.mlab.com:53784/eyeglasses'
let db = null
MongoClient.connect(dburl, (err, database) => {
  if (err) return console.log(err)
  db = database
})

router.get('/orders/:id', function(req, res, next) {
  res.sendFile(router.staticpath + '/tracking.html');
})

let status_cache = {}
router.get('/api/orders/:id', (req, res, next) => {
  let order = {}
  db.collection('orders').findOne({'order.id': req.params.id}, (err, results) => {
    if (err || !results) {
      console.log(err)
    }
    else {
      order = results.order

      // fake fulfillment lifecycle. This won't work with a scale group.
      // TODO: instead of in-memory cache do a mongodb update/increment of status
      if (order.id in status_cache) {
        status_cache[order.id] = status_cache[order.id] + 1
      }
      else {
        status_cache[order.id] = 0
      }
      order.status = status_cache[order.id]
    }
    res.setHeader('Content-Type', 'application/json')
    res.send(order)
  })
})

router.post('/api/orders', (req, res, next) => {
  db.collection('orders').save(req.body, (err, result) => {
    if (err) return console.log(err)

    res.setHeader('Content-Type', 'application/json')
    res.send({tracking_url: 'http://localhost:3000/orders/' + req.body.order.id})
  })
})

module.exports = router;
