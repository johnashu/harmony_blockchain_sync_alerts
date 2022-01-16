import logging as log

from bases.alerts_base import AlertsBase

from util.tools import check_hours_alert

from includes.config import envs


class Alerts(AlertsBase):
    def build_send_error_message(self, shard: int, *a, **kw) -> None:
        err_msg = self.build_error_message(*a, **kw)
        self.send_alert(
            f"Shard {shard} Behind -- {self.hostname}",
            err_msg,
            "danger",
            log.error,
            f"Shard {shard} Behind -- {self.hostname}",
        )

    def build_error_message(
        self,
        local_data_shard: dict,
        remote_data_shard: dict,
        blocks: int,
        _type: str = "shard",
    ):
        try:
            html = f"<strong>Local Epoch {local_data_shard[f'{_type}-chain-header']['epoch']}:</strong> {local_data_shard[f'{_type}-chain-header']['viewID']}\n<strong>Remote Epoch {remote_data_shard['shard-chain-header']['epoch']}:</strong> {remote_data_shard['shard-chain-header']['viewID']}\n<strong>Difference:</strong> {blocks}"
        except KeyError as e:
            msg = f"Problem finding KEY in [ build_error_message ] {e}\nlocal_data_shard  ::  {local_data_shard}\nremote_data_shard  ::  {remote_data_shard}"
            log.error(msg)
            return msg
        return html

    def generic_error(self, e: str):
        self.send_alert(
            f"Sync Script Error -- {self.hostname}",
            e,
            # f"Alert author\n\nError Message :: {e}",
            "danger",
            log.error,
            f"Sending ERROR Alert..ERROR  ::  {e}",
        )

    @check_hours_alert
    def happy_alert(
        self,
        shard: int,
        times_sent: dict,
        _send_alert: bool = False,
        first_run: bool = False,
    ) -> dict:

        if self.FULLY_SYNCED_NOTIFICATIONS and _send_alert:
            self.send_alert(
                f"Shard {shard} Synced -- {self.hostname}",
                f"",
                "info",
                log.info,
                f"Shard {shard} Synced -- {self.hostname}",
            )
        return times_sent

    def check_shard0_stuck(
        self, number: int, current_block: int, alert_sent: bool
    ) -> tuple:
        if number == current_block:
            if not alert_sent:
                if envs.SEND_STUCK_MSG:
                    self.send_alert(
                        "SHARD0 Stuck",
                        f"Shard0 is Stuck at Block [ {number} ] on Node {self.hostname} after {self.envs.FROZEN_SLEEP} seconds\nRestart script if you wish for this alert to continue",
                        "stuck",
                        log.info,
                        f"Shard0 is Stuck on Block [ {number} ] ",
                    )
                alert_sent = True
        else:
            current_block = number
            alert_sent = False
        return current_block, alert_sent
