import sys
import logging
import socket
import datetime

hostname = socket.gethostname()

from includes.config_utils import *

create_data_path((""))
file_handler = logging.FileHandler(filename=os.path.join("logs", "data.log"))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s",
    handlers=handlers,
    datefmt="%d-%m-%Y %H:%M:%S",
)
log = logging.getLogger()

envs = Envs()

VSTATS_API = "https://vstats.one/api/serversync"
OUR_SHARD = int(envs.SHARD)
HARMONY_FOLDER = envs.HARMONY_FOLDER

RUN_EVERY_X_MINUTES = int(envs.RUN_EVERY_X_MINUTES)
FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS = int(envs.FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS)
FULLY_SYNCED_NOTIFICATIONS = False

now = datetime.datetime.now() 
times = [x + now.hour for x in range(24) if x % FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS == 0]
times_sorted = sorted([ x - 24 if x > 23 else x for x in times])
times_sent = {
    x: False for x in times_sorted
}

if FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS > 0:
    FULLY_SYNCED_NOTIFICATIONS = True 
    # (mins in a day / RUN_EVERY_X_MINUTES) = number of loops in 24 hours / FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS
    # = STATUS to be performed on a multiple of this number


