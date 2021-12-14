import socket
from time import sleep

from util.send_alerts import send_alert, build_error_message
from util.commands import *

while True:
    try:
        log.info(f"Run sync check")
        # get remote stats for shard 0, then the #'d shard, if it's 0 just make it the same.
        shard_0_res, remote_data_shard_0 = process_command(latest_headers(s=0))
        if OUR_SHARD > 0:
            our_shard_res, remote_data_shard = process_command(
                latest_headers(s=OUR_SHARD)
            )
        else:
            remote_data_shard = remote_data_shard_0

        # get local server stats
        local_res, local_data_shard = process_command(latest_headers())

        # do math to see if we're in sync
        shard_0_blocks = do_maths_on_blocks(
            local_data_shard, remote_data_shard_0, _type="beacon"
        )
        if OUR_SHARD > 0:
            shard_n_blocks = do_maths_on_blocks(local_data_shard, remote_data_shard)

        # if lower blocks on shard 0
        if (
            shard_0_blocks <= -10 or shard_0_blocks >= 10
        ):  # Allow 10 block swing due to API lag between calls
            err_msg = build_error_message(
                local_data_shard, remote_data_shard_0, shard_0_blocks, _type="beacon"
            )
            send_alert(
                f"Shard 0 Behind -- {socket.gethostname()}",
                err_msg,
                "danger",
                log.error,
                "Sending OUT OF SYNC Alert..",
            )
        else:
            if FULLY_SYNCED_NOTIFICATIONS and (
                LOOP_COUNT % STATUS_NOTIFICATION_LOOP_COUNT == 0 or LOOP_COUNT == 0
            ):
                send_alert(
                    f"Shard 0 Synced -- {socket.gethostname()}",
                    f"",
                    "info",
                    log.info,
                    f"Shard 0 Synced -- {socket.gethostname()}",
                )

        # only if not on shard 0.
        if OUR_SHARD > 0:
            # if lower blocks on shard 3
            if (
                shard_n_blocks <= -10 or shard_n_blocks >= 10
            ):  # Allow 10 block swing due to API lag between calls
                err_msg = build_error_message(
                    local_data_shard, remote_data_shard, shard_n_blocks
                )
                send_alert(
                    f"Shard {OUR_SHARD} Behind -- {socket.gethostname()}",
                    err_msg,
                    "danger",
                    log.error,
                    "Sending OUT OF SYNC Alert..",
                )
            else:
                if FULLY_SYNCED_NOTIFICATIONS and (
                    LOOP_COUNT % STATUS_NOTIFICATION_LOOP_COUNT == 0 or LOOP_COUNT == 0
                ):
                    send_alert(
                        f"Shard {OUR_SHARD} Synced -- {socket.gethostname()}",
                        f"",
                        "info",
                        log.info,
                        "Sending SYNCED Alert..",
                    )

    except Exception as e:
        send_alert(
            "Sync Script Error",
            f"Alert author\n\nError Message :: {e}",
            "danger",
            log.error,
            "Sending ERROR Alert..",
        )
        log.error(e)
        log.error(f"Please fix me!")

    # Add to count
    LOOP_COUNT += 1
    # Delay by x seconds
    sleep(RUN_EVERY_X_MINUTES * 60)
    # Hot reload Env
    envs.load_envs()
