import logging as log
from includes.config import hostname

class AlertsBase:
    def __init__(self, VSTATS_API: str, connect_to_api: object, **kwargs) -> None:
        self.VSTATS_API = VSTATS_API
        self.connect_to_api = connect_to_api
        self.__dict__.update(kwargs)

    def send_to_vstats(self, subject: str, msg: str, alert_type: str, hostname: str = hostname) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "alert-type": alert_type,
            "subject": subject,
            "message": msg,
            "hostname": hostname,
        }
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)

    def send_alert(
        self, subject: str, msg: str, _type: str, log_level: log, log_msg: str
    ) -> None:
        log_level(log_msg)
        subject = f"{subject}"
        msg = f"{msg}"
        self.send_to_vstats(subject, msg, _type)
