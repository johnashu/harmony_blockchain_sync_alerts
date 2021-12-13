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

### Setup token
If you use validatortoolbox you can edit your ~/.easynode.env file to contain the following, replace `token` with your token:
- `VSTATS_BOT='token'`

If you do not use validatortoolbox edit your token into line 20 in place of `token`:
- `VSTATS_BOT='token'`

### Setup Service

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


```
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/harmony_blockchain_sync_alerts.service
sudo systemctl enable harmony_blockchain_sync_alerts.service
sudo service harmony_blockchain_sync_alerts start
sudo service harmony_blockchain_sync_alerts status
```
