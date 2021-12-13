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

COUNT = 0
VSTATS_API = "https://vstats.one/api/serversync"
OUR_SHARD = int(envs.SHARD)
HARMONY_FOLDER = envs.HARMONY_FOLDER
LOOP_EVERY_X_SECONDS = int(envs.LOOP_EVERY_X_SECONDS)
STATUS_NOTIFICATIONS_PER_DAY = int(envs.STATUS_NOTIFICATIONS_PER_DAY)
WORKING_NOTIFICATION_LOOP_COUNT = (86400 / LOOP_EVERY_X_SECONDS) / STATUS_NOTIFICATIONS_PER_DAY # 86400 seconds per day