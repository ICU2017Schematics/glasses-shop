server {
    listen 80;
    error_log /var/log/nginx/error.log;
    sendfile off;

    location /cat {
        proxy_pass http://CAT_SERVER;
    }

    location /cart {
        proxy_pass http://CART_SERVER;
    }
}