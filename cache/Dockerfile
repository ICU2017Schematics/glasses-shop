FROM nginx

ADD nginx.conf.tpl /tmp/nginx.conf.tpl
ADD run-nginx.sh /tmp/run-nginx.sh
RUN rm -f /etc/nginx/sites-enabled/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

CMD ["/tmp/run-nginx.sh"]
