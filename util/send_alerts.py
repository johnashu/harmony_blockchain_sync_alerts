import logging as log
from includes.config import envs, VSTATS_API
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


def build_error_message(
    local_data_shard: dict, remote_data_shard: dict, blocks: int, _type: str = "shard"
):
    return f"<strong>Local Epoch {local_data_shard[f'{_type}-chain-header']['epoch']}:</strong> {local_data_shard[f'{_type}-chain-header']['number']}\n<strong>Remote Epoch {remote_data_shard['shard-chain-header']['epoch']}:</strong> {remote_data_shard['shard-chain-header']['number']}\n<strong>Difference:</strong> {blocks}"
