from time import sleep

from util.commands import process_command, latest_headers, do_maths_on_blocks
from includes.config import *
from util.connect import connect_to_api
from util.send_alerts import Alerts


def run():
    while True:
        try:
            log.info(f"Run sync check")
            # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
            _, remote_data_shard_0 = process_command(latest_headers(s=0))
            if envs.SHARD > 0:
                _, remote_data_shard = process_command(latest_headers(s=envs.SHARD))
            else:
                remote_data_shard = remote_data_shard_0

            # get local server stats
            _, local_data_shard = process_command(latest_headers())

            # do math to see if we're in sync
            shard_0_blocks = do_maths_on_blocks(
                local_data_shard, remote_data_shard_0, _type="beacon"
            )
            if envs.SHARD > 0:
                shard_n_blocks = do_maths_on_blocks(local_data_shard, remote_data_shard)

            # if lower blocks on shard 0
            if (
                shard_0_blocks <= -10 or shard_0_blocks >= 10
            ):  # Allow 10 block swing due to API lag between calls
                alerts.build_send_error_message(
                    0,
                    local_data_shard,
                    remote_data_shard_0,
                    shard_0_blocks,
                    _type="beacon",
                )
            else:
                alerts.happy_alert(0)

            # only if not on shard 0.
            if envs.SHARD > 0:
                # if lower blocks on shard 3
                if (
                    shard_n_blocks <= -10 or shard_n_blocks >= 10
                ):  # Allow 10 block swing due to API lag between calls
                    alerts.build_send_error_message(
                        envs.SHARD, local_data_shard, remote_data_shard, shard_n_blocks
                    )
                else:
                    alerts.happy_alert(envs.SHARD)

        except Exception as e:
            alerts.generic_error(e)
            log.error(e)
            log.error(f"Please fix me!")

        # Add to count
        alerts.LOOP_COUNT += 1
        # Delay by x seconds
        sleep(envs.RUN_EVERY_X_MINUTES * 60)
        # sleep(2)
        # Hot reload Env
        envs.load_envs()


if __name__ == "__main__":

    alerts = Alerts(
        **dict(
            envs=envs,
            LOOP_COUNT=0,
            hostname=hostname,
            FULLY_SYNCED_NOTIFICATION_LOOP_COUNT=FULLY_SYNCED_NOTIFICATION_LOOP_COUNT,
            FULLY_SYNCED_NOTIFICATIONS=FULLY_SYNCED_NOTIFICATIONS,
            VSTATS_API=VSTATS_API,
            connect_to_api=connect_to_api,
        )
    )

    run()
