FROM nginx:mainline
RUN apt update
RUN apt install vlc -y
#COPY nginx.conf /etc/nginx/nginx.conf
RUN adduser --disabled-password --gecos "" alpine

# script
COPY vlc_stream.sh /opt/vlc_stream.sh
RUN chmod 755 /opt/vlc_stream.sh

# service
COPY vlc_stream.service /etc/systemd/system/vlc_stream.service
RUN systemctl enable --now vlc_stream
