FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
# COPY risos.hadeth.ir.crt /etc/nginx/
# COPY risos.hadeth.ir.key /etc/nginx/

# COPY . /etc/nginx/