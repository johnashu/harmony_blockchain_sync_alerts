import sys
import logging
import socket

hostname = socket.gethostname()

from config_utils import *

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

LOOP_COUNT = 0
VSTATS_API = "https://vstats.one/api/serversync"
OUR_SHARD = int(envs.SHARD)
HARMONY_FOLDER = envs.HARMONY_FOLDER

RUN_EVERY_X_MINUTES = int(envs.RUN_EVERY_X_MINUTES)
FULLY_SYNCED_NOTIFICATIONS_PER_DAY = int(envs.FULLY_SYNCED_NOTIFICATIONS_PER_DAY)
FULLY_SYNCED_NOTIFICATIONS = False

if FULLY_SYNCED_NOTIFICATIONS_PER_DAY > 0:
    FULLY_SYNCED_NOTIFICATIONS = True
    # (mins in a day / RUN_EVERY_X_MINUTES) = number of loops in 24 hours / FULLY_SYNCED_NOTIFICATIONS_PER_DAY
    # = STATUS to be performed on a multiple of this number
    STATUS_NOTIFICATION_LOOP_COUNT = int(
        (1440 / RUN_EVERY_X_MINUTES) / FULLY_SYNCED_NOTIFICATIONS_PER_DAY
    )  # 1440 minutes per day #
