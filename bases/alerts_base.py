import logging as log


class AlertsBase:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def send_to_vstats(self, subject: str, msg: str, alert_type: str) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "alert-type": alert_type,
            "subject": subject,
            "message": msg,
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
