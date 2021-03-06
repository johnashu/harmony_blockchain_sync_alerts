# Harmony Blockchain Sync Alerts

# vStats Alerts
This is an automated script that will periodically check your node block height against the blockchain. If there is a difference then a OUT OF SYNC ALERT will be sent. You may also setup an FULLY SYNCED ALERT to occur a set number of times per 24 hours to confirm nodes are fully synced.

If you are installing this on a newly created server which is still syncing to the blockchain then you may wish to pause the script after its installed or lower the frequency of the checks (in the .env file). Otherwise you will get frequent out of sync alerts until your caught up again. 

Example OUT OF SYNC ALERT:
```
🚨 Shard 0 Behind -- master-server 🚨
Local Epoch 793: 20320698
Remote Epoch 796: 20441501
Difference: -120803
```

Example FULLY SYNCED ALERT:
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
Send the command `/token` to the @vStatsBot on telegram to get your token.

Copy the token, as message on telegram will auto delete after 60 seconds.

### 3) Setup 
Install required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename .env.example to .env and edit the following variables:
```
cp .env.example .env
nano .env
```
> VSTATS_TOKEN: Add your token from vstats 

> SHARD:3 Add your chosen shard

> HARMONY_FOLDER:"" Add path containing .hmy ( run pwd in .hmy location to get full path ) e.g /home/serviceharmony/harmony

> RUN_EVERY_X_MINUTES:30 Define in minutes how often you would like the script to run and send an alert if behind

> FULLY_SYNCED_NOTIFICATIONS_PER_DAY:1 Define how often per 24 hours you would like an alert if you are fully synced. 0 = No status notifications

> SEND_STUCK_MSG=True # Check if Shard 0 is Stuck

> FROZEN_SLEEP=30 # Time to wait between checking for Shard0 being frozen. IN SECONDS

> RECEIVE_ERROR_MSG=True #Harmony RPC may return fequent errors and not be able to pull data. Do you want to receive error messages?

### 4) Test Script 
Test the .env variables and script is working as expected. 

Run the below from the script directory:

```
python3 alert.py
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


### Logs
Check logs to make sure the script is running as expected. 

### Misc
Start Service
```
sudo service harmony_blockchain_sync_alerts start
```

Stop Service
```
sudo service harmony_blockchain_sync_alerts stop
```

Status Check
```
sudo service harmony_blockchain_sync_alerts status
```
