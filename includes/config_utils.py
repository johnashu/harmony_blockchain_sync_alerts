import os
from dotenv import dotenv_values, find_dotenv
import logging as log


def create_data_path(pth: str, data_path: str = "logs") -> os.path:
    cwd = os.getcwd()
    p = os.path.join(cwd, data_path, pth)
    if not os.path.exists(p):
        os.mkdir(p)
    return p


class Envs:
    def __init__(self, **kw):
        self.load_envs()

    def load_envs(self):
        config = dotenv_values(find_dotenv())

        for k, v in config.items():
            if not v:
                err = f"No value for key {k} - Please update .env file!"
                log.error(err)
                raise ValueError(err)
            try:
                setattr(self, k, int(v))
            except (SyntaxError, ValueError):
                setattr(
                    self,
                    k,
                    True
                    if v.lower() == "true"
                    else False
                    if v.lower() == "false"
                    else v,
                )


def parse_times(FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS):
    times = []
    for x in range(24):
        try:
            if x % FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS == 0:
                times.append(x)
        except ZeroDivisionError:
            pass

    times_sorted = sorted([x - 24 if x > 24 else x for x in times])

    for x in times_sorted:
        if (
            (FULLY_SYNCED_NOTIFICATIONS_EVERY_X_HOURS > 12) or (x * 2 > 12)
        ) and 0 in times_sorted:
            times_sorted.remove(0)

    times_sent = {str(x): False for x in times_sorted}
    return times, times_sent
