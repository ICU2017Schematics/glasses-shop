#!/bin/bash
printenv

sed -e "s/CAT_SERVER/${CAT_SERVER}/" -e "s/CART_SERVER/${CART_SERVER}/" /tmp/nginx.conf.tpl > /etc/nginx/conf.d/nginx.conf
#cat /etc/nginx/conf.d/nginx.conf

up=`curl -s ${CAT_SERVER}/cat/__health__`
until [ "$up" = "1" ]; do
    echo "waiting for cat server ..."
    sleep 10s
    up=`curl -s ${CAT_SERVER}/cat/__health__`
done

up=`curl -s ${CART_SERVER}/cart/__health__`
until [ "$up" = "1" ]; do
    echo "waiting for cart server ..."
    sleep 10s
    up=`curl -s ${CART_SERVER}/cart/__health__`
done

echo "cat and cart servers are running."

nginx -g "daemon off;"

while true; do
    echo "nginx returned, going to sleep ..."
    sleep 1d
done
