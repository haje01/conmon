import os
import sys
import time
import logging
from logging import config as logconfig
from datetime import datetime

import yaml
import psutil
import servicemanager
import win32event
import win32service
import win32serviceutil
import click


SLEEP_SEC = 1
CFG_FNAME = 'config.yml'


def get_cfg_path():
    if getattr(sys, 'frozen', False):
        bdir = os.path.dirname(sys.executable)
    else:
        bdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bdir, CFG_FNAME)


def load_config():
    cfg_path = get_cfg_path()
    lip = lport = rip = rport = None
    with open(cfg_path) as f:
        data = yaml.load(f)
        if 'logger' in data:
            logconfig.dictConfig(data['logger'])
        if 'service' in data:
            adata = data['service']
            if adata is not None:
                lip = adata.get('lip')
                lport = adata.get('lport')
                rip = adata.get('rip')
                rport = adata.get('rport')
    return lip, lport, rip, rport


def log_process_info(p, con, connect_map):
    pid = p.pid

    try:
        name = p.name()
    except:
        logging.debug("Fail to get process name: {}".format(pid))
        return

    try:
        exe = p.exe()
    except:
        # logging.debug("Fail to get executable for pid: {}".format(pid))
        exe = None

    ppid = p.ppid()
    try:
        pname = psutil.Process(ppid).name() if ppid is not None else None
    except psutil.NoSuchProcess:
        pname = "_Destroyed_"

    try:
        username = p.username()
    except psutil.AccessDenied:
        username = "_AccessDenied_"

    ctime = datetime.fromtimestamp(p.create_time())

    lip, lport, rip, rport = None, None, None, None
    if len(con.laddr) == 2:
        lip, lport = con.laddr
    if len(con.raddr) == 2:
        rip, rport = con.raddr

    data = dict(pid=pid, ppid=ppid, name=name, pname=pname, username=username,
                exe=exe, ctime=ctime, lip=lip, lport=lport, rip=rip,
                rport=rport)
    key = (exe, pid, ppid)
    if key not in connect_map:
        connect_map[key] = True
        logging.info("\t{pid}\t{ppid}\t{name}\t{pname}\t{username}\t{exe}"
                     "\t{ctime}\t{lip}\t{lport}\t{rip}\t{rport}".
                     format(**data))


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


lip, lport, rip, rport = load_config()


def main(lip, lport, rip, rport):
    connect_map = {}
    for con in psutil.net_connections():
        if con.status != 'ESTABLISHED':
            continue
        if not check_filter(con, lip, lport, rip, rport):
            continue
        try:
            pid = psutil.Process(con.pid)
            log_process_info(pid, con, connect_map)
        except psutil.NoSuchProcess:
            pass


class ConmonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "conmon"
    _svc_display_name_ = "Connection Monitoring Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        servicemanager.LogInfoMsg("Service is stopping.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Service is starting.")
        rc = None
        log_header()
        while rc != win32event.WAIT_OBJECT_0:
            main(lip, lport, rip, rport)
            rc = win32event.WaitForSingleObject(self.hWaitStop, SLEEP_SEC *
                                                1000)
        log_footer()
        servicemanager.LogInfoMsg("Service is finished.")


@click.group()
def test_dummy():
    pass


def log_header():
    logging.critical("=========== Start connection monitoring ===========")
    cfg_path = get_cfg_path()
    logging.critical("Config file: '{}', lip: {}, lport: {}, rip: {}, "
                     "rport: {}".format(cfg_path, lip, lport, rip, rport))


def log_footer():
    logging.critical("=========== Finish connection monitoring ===========")


@click.command()
@click.option("--lip", help="target local ip")
@click.option("--lport", type=int, help="target local port")
@click.option("--rip", help="target remote ip")
@click.option("--rport", type=int, help="target remote port")
def test(lip, lport, rip, rport):
    log_header()
    while True:
        main(lip, lport, rip, rport)
        time.sleep(SLEEP_SEC)

test_dummy.add_command(test)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ConmonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        cmd = sys.argv[1]
        if cmd == 'test':
            test_dummy()
        else:
            win32serviceutil.HandleCommandLine(ConmonService)
