from time import sleep

from util.commands import process_command, latest_headers, do_maths_on_blocks
from includes.config import *
from util.connect import connect_to_api
from util.send_alerts import Alerts


def run(times_sent: dict):
    start_time = datetime.datetime.now()
    current_block = 0
    alert_sent = False
    while True:
        try:
            log.info(f"Run sync check")
            # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
            res, remote_data_shard_0 = process_command(latest_headers(s=0))
            if not res:
                alerts.generic_error(remote_data_shard_0)
            else:
                # // Check Shard 0 is not stuck
                res, main_rpc_data = process_command(latest_headers())
                if not res:
                    alerts.generic_error(main_rpc_data)
                else:

                    number = int(main_rpc_data["beacon-chain-header"]["number"], 16)
                    current_block, alert_sent = alerts.check_shard0_stuck(
                        number, current_block, alert_sent
                    )

                # is it time to check?
                time_check = datetime.datetime.now()
                time_calc = (time_check - start_time).seconds

                if time_calc >= (envs.RUN_EVERY_X_MINUTES * 60):
                    start_time = time_check
                    if envs.SHARD == 0:
                        remote_data_shard = remote_data_shard_0
                    else:
                        res2, remote_data_shard = process_command(
                            latest_headers(s=envs.SHARD)
                        )
                    if not res2:
                        alerts.generic_error(remote_data_shard)
                    else:
                        # get local server stats
                        _, local_data_shard = process_command(latest_headers())

                        # do math to see if we're in sync -
                        # Change to int to throw error and send error alert with the message received.
                        shard_0_blocks = int(
                            do_maths_on_blocks(
                                local_data_shard, remote_data_shard_0, _type="beacon"
                            )
                        )
                        if envs.SHARD > 0:
                            shard_n_blocks = int(
                                do_maths_on_blocks(local_data_shard, remote_data_shard)
                            )

                        # if lower blocks on shard 0
                        if (
                            shard_0_blocks
                            <= -20
                            # shard_0_blocks <= -20 or shard_0_blocks >= 10
                        ):  # Allow 10 block swing due to API lag between calls
                            alerts.build_send_error_message(
                                0,
                                local_data_shard,
                                remote_data_shard_0,
                                shard_0_blocks,
                                _type="beacon",
                            )
                        else:
                            times_sent = alerts.happy_alert(0, times_sent)

                        # only if not on shard 0.
                        if envs.SHARD > 0:
                            # if lower blocks on shard 3
                            if (
                                shard_n_blocks
                                <= -20
                                # shard_n_blocks <= -20 or shard_n_blocks >= 10
                            ):  # Allow 10 block swing due to API lag between calls
                                alerts.build_send_error_message(
                                    envs.SHARD,
                                    local_data_shard,
                                    remote_data_shard,
                                    shard_n_blocks,
                                )
                            else:
                                times_sent = alerts.happy_alert(envs.SHARD, times_sent)

        except Exception as e:
            alerts.generic_error(e)
            log.error(e)
            log.error(f"Please fix me!")

        # Delay by x seconds
        sleep(0.1)
        # sleep(2)
        # Hot reload Env
        envs.load_envs()


if __name__ == "__main__":
    alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)
    run(times_sent)

    # alerts.send_alert(
    #     "TEST",
    #     f'TEST ',
    #     "danger",
    #     log.info,
    #     f"TEST",
    # )
