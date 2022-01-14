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
    format="%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s",
    handlers=handlers,
    datefmt="%d-%m-%Y %H:%M:%S",
)
log = logging.getLogger()

envs = Envs()

VSTATS_API = "https://vstats.one/api/serversync"
FULLY_SYNCED_NOTIFICATIONS = False

if envs.FULLY_SYNCED_NOTIFICATIONS_PER_DAY > 0:
    FULLY_SYNCED_NOTIFICATIONS = True
    # (mins in a day / envs.RUN_EVERY_X_MINUTES) = number of loops in 24 hours / envs.FULLY_SYNCED_NOTIFICATIONS_PER_DAY
    # = STATUS to be performed on a multiple of this number
    FULLY_SYNCED_NOTIFICATION_LOOP_COUNT = int(
        (1440 / envs.RUN_EVERY_X_MINUTES) / envs.FULLY_SYNCED_NOTIFICATIONS_PER_DAY
    )  # 1440 minutes per day #

    # this can potentially evaluate to 0. Sanitise this value.
    if FULLY_SYNCED_NOTIFICATION_LOOP_COUNT <= 0:
        FULLY_SYNCED_NOTIFICATION_LOOP_COUNT = 1

alerts_context = dict(
    envs=envs,
    LOOP_COUNT=0,
    hostname=hostname,
    FULLY_SYNCED_NOTIFICATION_LOOP_COUNT=FULLY_SYNCED_NOTIFICATION_LOOP_COUNT,
    FULLY_SYNCED_NOTIFICATIONS=FULLY_SYNCED_NOTIFICATIONS,
)

frozen_cmd = (
    """./hmy blockchain latest-headers | jq .result | jq '.["beacon-chain-header"]'  | jq -r .number | xargs printf "%d\n"""
    ""
)
FROZEN_SLEEP = 10