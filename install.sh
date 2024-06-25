#! /bin/bash

#sudo useradd -m minecraft
#sudo usermod -a -G minecraft $USER
#logout
#sudo chown -R minecraft: /home/minecraft/

apt update
apt install wget screen openssl python3-pip -y

wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb -O libssl1.1.deb
dpkg -i libssl1.1.deb
rm libssl1.1.deb

python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 install.py

chmod +x ./MinecraftServer/bedrock_server
chmod +x ./MinecraftServer/start_server.sh
chmod +x ./MinecraftServer/stop_server.sh
cp ./MinecraftServer/MCServer.service /etc/systemd/system/MCServer.service

#sudo chown -R minecraft: /home/minecraft

ufw allow 19132:19133/tcp
ufw allow 19132:19133/udp
ufw enable

systemctl enable MCServer
systemctl start MCServer