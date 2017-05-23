import logging
import time
from logging import config
from datetime import datetime

import yaml
import psutil
import click

exe_map = {}

with open('logcfg.yml') as f:
    data = yaml.load(f)
    config.dictConfig(data)


def log_process_info(p, con):
    pid = p.pid
    try:
        exe = p.exe()
    except:
        # logging.debug("Fail to get executable for pid: {}".format(pid))
        return

    if exe not in exe_map:
        exe_map[exe] = True
        logging.warning("First connection from {}".format(exe))

    ppid = p.ppid()
    pname = psutil.Process(con.pid).name() if ppid is not None else None
    name = p.name()
    username = p.username()
    ctime = datetime.fromtimestamp(p.create_time())
    logging.info("pid: {}, ppid: {}, name: {}, pname: {}, username: {}, exe:"
                 " {}, ctime: {}, connection: {}".format(pid, ppid, name,
                                                         pname, username, exe,
                                                         ctime, con))


def check_filter(con, lip, lport, rip, rport):
    # check source condition
    if lip is not None or lport is not None:
        if len(con.laddr) == 0:
            return False
    if lip is not None:
        if con.laddr[0] != lip:
            return False
    if lport is not None:
        if con.laddr[1] != lport:
            return False

    # check dest condition
    if rip is not None or rport is not None:
        if len(con.raddr) == 0:
            return False
    if rip is not None:
        if con.raddr[0] != rip:
            return False
    if rport is not None:
        if con.raddr[1] != rport:
            return False

    return True


@click.command()
@click.option("--lip", help="target local ip")
@click.option("--lport", type=int, help="target local port")
@click.option("--rip", help="target remote ip")
@click.option("--rport", type=int, help="target remote port")
def main(lip, lport, rip, rport):
    logging.critical("=========== Start connection monitoring ===========")
    logging.critical("lip: {}, lport: {}, rip: {}, rport: {}"
                     .format(lip, lport, rip, rport))
    while True:
        for con in psutil.net_connections():
            if con.status != 'ESTABLISHED':
                continue
            if not check_filter(con, lip, lport, rip, rport):
                continue
            try:
                pid = psutil.Process(con.pid)
                log_process_info(pid, con)
            except psutil.NoSuchProcess:
                pass
        time.sleep(1)


if __name__ == '__main__':
    main()
