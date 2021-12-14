import logging as log
from includes.config import (
    envs,
    VSTATS_API,
    hostname,
    FULLY_SYNCED_NOTIFICATIONS,
    FULLY_SYNCED_NOTIFICATION_LOOP_COUNT,
    LOOP_COUNT,
    OUR_SHARD,
)

from util.connect import connect_to_api


def send_to_vstats(subject: str, msg: str, alert_type: str) -> None:
    j = {
        "api_token": envs.VSTATS_TOKEN,
        "alert-type": alert_type,
        "subject": subject,
        "message": msg,
    }
    full, _, _ = connect_to_api("", VSTATS_API, "", j=j)
    log.info(full)


def send_alert(
    subject: str, msg: str, _type: str, log_level: log, log_msg: str
) -> None:
    log_level(log_msg)
    subject = f"{subject}"
    msg = f"{msg}"
    send_to_vstats(subject, msg, _type)


def build_send_error_message(shard: int, *a, **kw) -> None:
    err_msg = build_error_message(*a, **kw)
    send_alert(
        f"Shard {shard} Behind -- {hostname}",
        err_msg,
        "danger",
        log.error,
        "Sending OUT OF SYNC Alert..",
    )


def build_error_message(
    local_data_shard: dict, remote_data_shard: dict, blocks: int, _type: str = "shard"
):
    return f"<strong>Local Epoch {local_data_shard[f'{_type}-chain-header']['epoch']}:</strong> {local_data_shard[f'{_type}-chain-header']['viewID']}\n<strong>Remote Epoch {remote_data_shard['shard-chain-header']['epoch']}:</strong> {remote_data_shard['shard-chain-header']['viewID']}\n<strong>Difference:</strong> {blocks}"


def generic_error(e: str):
    send_alert(
        "Sync Script Error",
        f"Alert author\n\nError Message :: {e}",
        "danger",
        log.error,
        "Sending ERROR Alert..",
    )


def happy_alert(shard: int) -> None:
 
    send_alert(
        f"Shard {shard} Synced -- {hostname}",
        f"",
        "info",
        log.info,
        f"Shard {shard} Synced -- {hostname}",
    )
