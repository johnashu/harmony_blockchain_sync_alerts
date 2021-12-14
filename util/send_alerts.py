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

def send_out_of_sync_alert(subject: str, msg: str) -> None:
    log.error("Sending OUT OF SYNC Alert..")
    subject = f"{subject}"
    msg = f"{msg}"
    send_to_vstats(subject, msg, "danger")
    
def send_error_alert(e: str, subject: str, msg: str) -> None:
    log.error("Sending ERROR Alert..")
    subject = f"{subject}"
    msg = f"{msg}"
    send_to_vstats(subject, msg, "danger")


def send_synced_alert(subject: str, msg: str, servername: str, diff: str) -> None:
    log.info("Sending SYNCED Alert..")
    subject = f"{subject}"
    msg = f"{msg}"
    servername = f"{servername}"
    diff = f"{diff}"
    alert_type = "info"
    #send_to_vstats(subject, msg,server,difference, "info")
    j = {
        "api_token": envs.VSTATS_TOKEN,
        "alert-type": alert_type,
        "subject": subject,
        "message": msg,
        "diff": diff,
        "servername": servername,
    }
    full, _, _ = connect_to_api("", VSTATS_API, "", j=j)
    log.info(full)
    