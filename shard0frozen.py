from time import sleep

from util.commands import process_command, latest_headers, do_maths_on_blocks
from includes.config import *
from util.connect import connect_to_api
from util.send_alerts import Alerts


def run_stuck_check():
    current_block = 0
    alert_sent = False
    while True:
        try:
            log.info(f"Run shard0 check")
            # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
            res, shard0_latest_headers = process_command(latest_headers())

            if not res:
                alerts.generic_error(shard0_latest_headers)
            else:                
                number = int(shard0_latest_headers["beacon-chain-header"]["number"], 16)
                log.info(f"number = {number}\ncurrent_block = {current_block}")
                log.info(f"number == current_block  ::  {number == current_block}")
                if (number == current_block) and not alert_sent:
                    alerts.send_alert(
                        "SHARD0 Stuck",
                        f"Shard0 is Stuck at Block [ {number} ] on Node {hostname}",
                        "stuck",
                        log.info,
                        f"Shard0 is Stuck on Block [ {number} ] ",
                    )
                    alert_sent = True
                else:
                    current_block = number
                    alert_sent = False

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
