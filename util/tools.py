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


def check_hours_alert(function_to_decorate):
    def wrapper(self, shard, times_sent, _send_alert=False, first_run: bool = False):
        now = datetime.datetime.now()
        h = str(now.hour)
        if not first_run:
            if int(h) in times:
                if not times_sent[h]:
                    times_sent[h] = True
                    _send_alert = True
            if all([times_sent[x] for x in times_sent]):
                times_sent = {str(x): False for x in times}

        return function_to_decorate(
            self, shard, times_sent, _send_alert=_send_alert, first_run=first_run
        )

    return wrapper
