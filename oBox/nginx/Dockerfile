FROM nginx:alpine

COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY ./www/index.html /usr/share/nginx/html/index.html
COPY ./www/favicon.ico /usr/share/nginx/html/favicon.ico
COPY ./ca-certs/* /etc/ssl/certs/
RUN mkdir -p /opt/nginx/pki
COPY ./own-cert/nginx-cert.pem /opt/nginx/pki/
COPY ./own-cert/nginx-key.pem /opt/nginx/pki/

ENV DOLLAR="$"

# Important Note: Modify also environment variables in file .env!

# This is the host name used to access main menu (nginx is listening to it):
ENV REVERSE_PROXY_HOST obox.testco.opcfy.io

# This is keycloak host name. 
ENV KEYCLOAK_HOST keycloak.testco.opcfy.io

# the rest of host names might be used only internally and left as is.
ENV OAUTH2PROXY_HOST oauth2proxy
ENV OVL_HOST ovl.testco.opcfy.io
ENV DEVICE_GATEWAY_HOST devicegateway
ENV FORGE_HOST forge
ENV INFLUXDB_HOST influxdb2
ENV GRAFANA_HOST grafana
ENV PGADMIN_HOST pgadmin
ENV EKUIPER_MANAGER_HOST ekuiper-manager
ENV TIMESERIESADMIN_HOST timeseriesadmin

CMD envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf & nginx -g 'daemon off;'
# | tail -f /dev/null