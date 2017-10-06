#!/bin/bash
cd ship
npm install
npm run build
cd ../website
npm install
npm run build
cd ..
docker build -t cloudu2017/cat  ./cat
docker build -t cloudu2017/cart ./cart
docker build -t cloudu2017/gateway   ./gateway
docker build -t cloudu2017/ship   ./ship
docker build -t cloudu2017/swebsite   ./website
