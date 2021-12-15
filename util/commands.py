import json
from subprocess import PIPE, run
import logging as log
from includes.config import envs


def process_command(cmd: list) -> json:
    result = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out = result.stdout
    err = result.stderr
    try:
        rtn_json = json.loads(out)
        return True, rtn_json["result"]
    except json.JSONDecodeError as e:
        log.error(e)
        return False, {"Error": e, "stdout": out, "stderr": err}


def latest_headers(s: int = -1) -> list:
    node = ""
    if s != -1:
        node = f"--node=https://api.s{s}.t.hmny.io"
    return [f"{envs.HARMONY_FOLDER}/hmy", "blockchain", "latest-headers", node]


def do_maths_on_blocks(
    local_data_shard: dict, remote_data_shard: dict, _type: str = "shard"
) -> int:
    try:
        result = int(local_data_shard[f"{_type}-chain-header"]["viewID"]) - int(
            remote_data_shard[f"shard-chain-header"]["viewID"]
        )
    except KeyError as e:
        msg = f"Problem finding KEY in [ do_maths_on_blocks ] {e}\nlocal_data_shard  ::  {local_data_shard}\nremote_data_shard  ::  {remote_data_shard}"
        log.error(msg)
        return msg

    return result
