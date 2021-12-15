import logging as log

from bases.alerts_base import AlertsBase


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
        return f"<strong>Local Epoch {local_data_shard[f'{_type}-chain-header']['epoch']}:</strong> {local_data_shard[f'{_type}-chain-header']['viewID']}\n<strong>Remote Epoch {remote_data_shard['shard-chain-header']['epoch']}:</strong> {remote_data_shard['shard-chain-header']['viewID']}\n<strong>Difference:</strong> {blocks}"

    def generic_error(self, e: str):
        self.send_alert(
            "Sync Script Error",
            f"Alert author\n\nError Message :: {e}",
            "danger",
            log.error,
            "Sending ERROR Alert..",
        )

    def happy_alert(self, shard: int):
        log.info(self.LOOP_COUNT)
        if self.FULLY_SYNCED_NOTIFICATIONS and (
            self.LOOP_COUNT % self.FULLY_SYNCED_NOTIFICATION_LOOP_COUNT == 0
            or self.LOOP_COUNT == 0
        ):
            self.send_alert(
                f"Shard {shard} Synced -- {self.hostname}",
                f"",
                "info",
                log.info,
                f"Shard {shard} Synced -- {self.hostname}",
            )
