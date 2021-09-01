FROM redis:alpine
RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app /etc
USER app
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]