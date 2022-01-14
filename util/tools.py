import subprocess
from includes.config import times, datetime

def process(cmd: str) -> subprocess:
    o, e = subprocess.Popen(
        cmd,
        shell=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    return o, e


def flatten(d: dict) -> None:
    """Flatten a nested dictionary.

    Args:
        d (dict): nested dictionary to flatten

    Returns:
        dict: flattened dictionary.
    """
    out = {}
    if d:
        if isinstance(d, str):
            import ast

            try:
                d = ast.literal_eval(d)
            except (ValueError, SyntaxError):
                pass
        try:
            for key, val in d.items():
                if isinstance(val, dict):
                    val = [val]
                if isinstance(val, list):
                    for subdict in val:
                        deeper = flatten(subdict).items()
                        out.update(
                            {
                                key2: val2
                                for key2, val2 in deeper
                                if key2 not in out.keys()
                            }
                        )
                else:
                    out[key] = val
        except AttributeError as e:
            pass
    return out


def send_synced_notification(times_sent: dict) -> tuple:
    send_happy_alert = False
    now = datetime.datetime.now()    
    h = now.hour
    if h in times and not times_sent[h]:
        times_sent[h] = True
        send_happy_alert = True
        if all([times_sent[x] for x in times_sent]):
            times_sent = {
                    x: False for x in times
                }
    return times_sent, send_happy_alert