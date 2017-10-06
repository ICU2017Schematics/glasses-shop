#!/bin/bash

cd ship
npm run build
cd ../website
npm run build
cd ..
docker build -t mkubik/cat  ./cat
docker build -t mkubik/cart ./cart
docker build -t mkubik/gateway   ./gateway
docker build -t mkubik/ship   ./ship
docker build -t mkubik/website   ./website

docker push mkubik/cat
docker push mkubik/cart
docker push mkubik/gateway
docker push mkubik/ship
docker push mkubik/website
