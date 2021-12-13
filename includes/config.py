import sys
import logging
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

LOOP_COUNT = 0
VSTATS_API = "https://vstats.one/api/serversync"
OUR_SHARD = int(envs.SHARD)
HARMONY_FOLDER = envs.HARMONY_FOLDER

LOOP_EVERY_X_MINUTES = int(envs.LOOP_EVERY_X_MINUTES)
STATUS_NOTIFICATIONS_PER_DAY = int(envs.STATUS_NOTIFICATIONS_PER_DAY)
STATUS_NOTIFICATIONS = False

if STATUS_NOTIFICATIONS_PER_DAY > 0:
    STATUS_NOTIFICATIONS = True
    # (mins in a day / LOOP_EVERY_X_MINUTES) = number of loops in 24 hours / STATUS_NOTIFICATIONS_PER_DAY  
    # = STATUS to be performed on a multiple of this number 
    STATUS_NOTIFICATION_LOOP_COUNT = (1440 / LOOP_EVERY_X_MINUTES) / STATUS_NOTIFICATIONS_PER_DAY # 1440 minutes per day #
    
