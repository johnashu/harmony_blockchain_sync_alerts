# Harmony Blockchain Sync Alerts

# vStats Alerts
This is an automated script that will periodically check your node block height against the blockchain. If there is a difference then an alert will be sent. You may also setup a Status alert to occur a set number of times per 24 hours to confirm nodes are fully synced.

If you are installing this on a newly created server which is still syncing to the blockchain then you may wish to pause the script after its installed or lower the frequency of the checks (in the .env file). Otherwise you will get frequent out of sync alerts until your caught up again. 

Example out of sync alert:
```
🚨 Shard 0 Behind -- master-server 🚨
Local Epoch 793: 20320698
Remote Epoch 796: 20441501
Difference: -120803
```

Example Status alert:
```
🔶 Shard 3 Synced -- master-server 🔶
```

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

Copy the token, as message on telegram will auto delete after 60 seconds.

### 3) Setup 
Install required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename .env.example to .env and edit the following variables:

> VSTATS_TOKEN: Add your token from vstats 

> SHARD: Add your chosen shard

> LOOP_EVERY_X_MINUTES: Define in minutes how often you would like the script to run

> STATUS_NOTIFICATIONS_PER_DAY: Define how often per 24 hours you would like a status update ( assuming fully synced ). 0 = No status notifications

> HARMONY_FOLDER: Add path containing .hmy ( run pwd in .hmy location to get full path ) e.g /home/serviceharmony/harmony_blockchain_sync_alerts

### 4) Test Script 
Test the .env variables and script is working as expected. 

Run the below from the script directory:

```
python3 alerts.py
```

Alerts on screen AND vStatsBot should appear. Once successful, please cancel the script ( CTRL + C ) and move onto the next step.

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

`tmux new-session -s syncscript`
`cd ~/harmony_blockchain_sync_alerts/`
`python3 alert.py`


### 6) Logs
Check logs to make sure the script is running as expected. 
