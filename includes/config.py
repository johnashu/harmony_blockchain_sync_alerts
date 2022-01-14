import sys
import logging
import socket

hostname = socket.gethostname()

from includes.config_utils import *

create_data_path((""))
file_handler = logging.FileHandler(filename=os.path.join("logs", "data.log"))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] <%(funcName)s : %(lineno)s> %(message)s",
    handlers=handlers,
    datefmt="%d-%m-%Y %H:%M:%S",
)
log = logging.getLogger()

envs = Envs()

VSTATS_API = "https://vstats.one/api/serversync"
FULLY_SYNCED_NOTIFICATIONS = False

import datetime

FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS = 24 // envs.FULLY_SYNCED_NOTIFICATIONS_PER_DAY

times, times_sent = parse_times(FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS)

if FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS > 0:
    FULLY_SYNCED_NOTIFICATIONS = True

alerts_context = dict(
    envs=envs,
    LOOP_COUNT=0,
    hostname=hostname,
    FULLY_SYNCED_NOTIFICATIONS=FULLY_SYNCED_NOTIFICATIONS,
)

FROZEN_SLEEP = 30
