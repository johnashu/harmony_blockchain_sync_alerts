from time import sleep

from util.commands import process_command, latest_headers, do_maths_on_blocks
from includes.config import *
from util.connect import connect_to_api
from util.send_alerts import Alerts


def run_stuck_check():
    current_block = 0
    while True:
        try:
            log.info(f"Run shard0 check")
            # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
            res, shard0_latest_headers = process_command(frozen_cmd)
            if not res:
                alerts.generic_error(shard0_latest_headers)
            else:
                if shard0_latest_headers == current_block: 
                    alerts.send_alert(
                        "SHARD0 Stuck",
                        f"Shard0 is Stuck on Block [ {shard0_latest_headers} ] ",
                        "stuck",
                        log.info,
                        f"Shard0 is Stuck on Block [ {shard0_latest_headers} ] ",
                    )
                else:
                    current_block = shard0_latest_headers

        except Exception as e:
            alerts.generic_error(e)
            log.error(e)
            log.error(f"Please fix me!")

        # Delay by x seconds
        sleep(FROZEN_SLEEP)

        # Hot reload Env
        envs.load_envs()


if __name__ == "__main__":
    alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)
    run_stuck_check()

    # alerts.send_alert(
    #     "TEST",
    #     f'TEST ',
    #     "stuck",
    #     log.info,
    #     f"TEST",
    # )
