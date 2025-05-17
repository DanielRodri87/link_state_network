FROM python:3.10-slim

WORKDIR /app

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    iputils-ping \
    traceroute  

CMD ["/app/start.sh"]