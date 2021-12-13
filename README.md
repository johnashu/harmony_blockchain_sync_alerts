# harmony_blockchain_sync_alerts

# vStats alerts

### Get a token
Send the command `/serversynctoken` to the @vStatsBot on telegram to get your token.

### Download the alert.py script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/DavidWhicker/harmony_blockchain_sync_alerts.git
```

### Setup 
Rename .env.example to .env

Add your token: VSTATS_TOKEN

Add your chosen shard: SHARD

Define in minutes how often you would like the script to run: LOOP_EVERY_X_MINUTES

Define how often per 24 hours you would like a status update: STATUS_NOTIFICATIONS_PER_DAY

Add location of .hmy ( run pwd in .hmy location to get full path ): HARMONY_FOLDER

### Test Script 
Test the .env variables and script are running as expected. Run python3 alerts.py from the script directory. Alerts on screen AND vStatsBot should appear. 

### Setup Service
Now setup script to run as a service in the background. 

Run the following with root privileges. Please note: add correct info for USER & PATH TO SCRIPT

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
WorkingDirectory=<PATH TO SCRIPT eg. /home/serviceharmony/harmony_blockchain_sync_alerts>
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

### Logs
Check logs to make sure the script is running as expected. 
