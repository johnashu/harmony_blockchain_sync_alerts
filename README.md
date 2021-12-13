# Harmony Blockchain Sync Alerts

# vStats Alerts

### 1) Download the script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/DavidWhicker/harmony_blockchain_sync_alerts.git
cd harmony_blockchain_sync_alerts
```
To update use `git pull`

### 2) Get a token
Send the command `/serversynctoken` to the @vStatsBot on telegram to get your token.

Save token as message on telegram will auto delete after 60 seconds.

### 3) Setup 
Instal required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename .env.example to .env and edit the following variables:

> VSTATS_TOKEN: Add your token from vstats 

> SHARD: Add your chosen shard

> LOOP_EVERY_X_MINUTES: Define in minutes how often you would like the script to run

> STATUS_NOTIFICATIONS_PER_DAY: Define how often per 24 hours you would like a status update ( assuming fully synced ). 0 = no status notifications

> HARMONY_FOLDER: Add path containing .hmy ( run pwd in .hmy location to get full path ) e.g /home/serviceharmony/harmony_blockchain_sync_alerts

### 4) Test Script 
Test the .env variables and script is working as expected. 

Run the below from the script directory:

```
python3 alerts.py
```

Alerts on screen AND vStatsBot should appear. 

### 5) Setup Service
Now setup script to run as a service in the background. 

Run the following with root privileges. If you do not have access with root then you may setup a tmux session ( see: Alternative Setup - Tmux ).

Please note: add correct info for < USER > & < PATH TO SCRIPT >

```
cat<<-EOF > /etc/systemd/system/harmony_blockchain_sync_alerts.service
[Unit]
Description=harmony_blockchain_sync_alerts daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=<USER>
WorkingDirectory=<PATH TO SCRIPT>
ExecStart=python3 alert.py
SyslogIdentifier=harmony_blockchain_sync_alerts
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF
```
Followed by:

```
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/harmony_blockchain_sync_alerts.service
sudo systemctl enable harmony_blockchain_sync_alerts.service
sudo service harmony_blockchain_sync_alerts start
sudo service harmony_blockchain_sync_alerts status
```

### 5b) Alternative Setup - Tmux
```
tmux new-session -s syncscript
cd ~/harmony_blockchain_sync_alerts
python3 alert.py
```

### 6) Logs
Check logs to make sure the script is running as expected. 
