import json
import socket
import requests
import os
from subprocess import Popen, PIPE, run
from ast import literal_eval
from time import sleep
from includes.config import *
from util.send_alerts import (
    send_synced_alert,
    send_out_of_sync_alert,
    send_error_alert,
)


while True:
    try: 
       # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
       remote_shard_0 = [f'{HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
       result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
       remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
       if OUR_SHARD > 0:
           remote_shard = [f'{HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{OUR_SHARD}.t.hmny.io']
           result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
           remote_data_shard = json.loads(result_remote_shard.stdout)
       else:
           remote_shard = remote_data_shard_0
           result_remote_shard = result_remote_shard_0
           remote_data_shard = remote_data_shard_0
       
       # get local server stats
       local_shard = [f'{HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers']
       result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
       local_data_shard = json.loads(result_local_shard.stdout)
         
      
       # do math to see if we're in sync
       shard_0_blocks = literal_eval(local_data_shard['result']['beacon-chain-header']['number']) - literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])
       if OUR_SHARD > 0:
           shard_n_blocks = literal_eval(local_data_shard['result']['shard-chain-header']['number']) - literal_eval(remote_data_shard['result']['shard-chain-header']['number'])
       
       # if lower blocks on shard 0
       if shard_0_blocks <= -10 or shard_0_blocks >= 10:
           send_out_of_sync_alert('Shard 0 Behind',f"<strong>Server:</strong> {socket.gethostname()}\n<strong>Local Epoch {local_data_shard['result']['beacon-chain-header']['epoch']} Block:</strong> {literal_eval(local_data_shard['result']['beacon-chain-header']['number'])}\n<strong>Remote Epoch {remote_data_shard_0['result']['shard-chain-header']['epoch']} Block:</strong> {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}\n<strong>Off by:</strong> {shard_0_blocks}")
           log.info(f"test2a")
       else:
           if COUNT % WORKING_NOTIFICATION_LOOP_COUNT == 0 or COUNT == 0:
               send_synced_alert(f'Shard 0 Synced -- {socket.gethostname()}',f"")
       
       # only if not on shard 0.
       if OUR_SHARD > 0:
       # if lower blocks on shard 3
           if shard_n_blocks <= -10 or shard_n_blocks >= 10:
               send_out_of_sync_alert(f'Shard {OUR_SHARD} Behind',f"<strong>Server:</strong> {socket.gethostname()}\n<strong>Local Epoch {local_data_shard['result']['shard-chain-header']['epoch']} Block:</strong> {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}\n<strong>Remote Epoch {remote_data_shard['result']['shard-chain-header']['epoch']} Block:</strong> {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}\nOff by:</strong> {shard_n_blocks}")
           else:
               if COUNT % WORKING_NOTIFICATION_LOOP_COUNT == 0 or COUNT == 0:
                   send_synced_alert(f'Shard {OUR_SHARD} Synced -- {socket.gethostname()}',f"")
                   
    except Exception as e:
        send_error_alert(e, "Error", f"")
        log.error(e)
        log.error( f"Please fix me!")
    
    # Add to count
    COUNT += 1
    # Delay by x seconds
    sleep(LOOP_EVERY_X_SECONDS)
    # Hot reload Env
    envs.load_envs()
    
