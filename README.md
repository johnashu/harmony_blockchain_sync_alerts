# harmony_blockchain_sync_alerts

# vStats alerts

### Get a token
Send the command `/easynodetoken` to the @vStatsBot on telegram to get your token.

### Download the alert.py script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/DavidWhicker/harmony_blockchain_sync_alerts.git
```

### Setup 
Add your token to the .env file. 
Configure how all other variables in .env file. 
To get working directory use pwd

### Test Script 
Test the .env variables and script are running as expected. Run python3 alerts.py from the script directory. Alerts on screen AND vStatsBot should appear. 

### Setup Service
Now setup script to run as a service in the background. 

Run the following with root privileges

```
cat<<-EOF > /etc/systemd/system/harmony_blockchain_sync_alerts.service
[Unit]
Description=harmony_blockchain_sync_alerts daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=serviceharmony
WorkingDirectory=/home/serviceharmony/harmony_blockchain_sync_alerts
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
