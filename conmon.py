import os
import sys
import logging
from logging import config as logconfig
from datetime import datetime
import socket
import struct

import yaml
import psutil
import servicemanager
import win32event
import win32service
import win32serviceutil
import click
import errno
import netifaces


SLEEP_SEC = 1
CFG_FNAME = 'config.yml'
RECV_SIZE = 65565


def get_first_iface_addr():
    ifs = netifaces.interfaces()
    return netifaces.ifaddresses(ifs[0])[2][0]['addr']


def prepare_sniff(hostip):
    logging.critical("\t# Target host IP: {}".format(hostip))
    # create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        # s.setblocking(0)
        s.bind((hostip, 0))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    except socket.error, msg:
        logging.error('# Socket could not be created. Error Code : ' +
                      str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    return s


def sniff(s, hostip, hport, sip, sport):
    if False:
        try:
            packet = s.recv(RECV_SIZE)
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                pass
            else:
                logging.error("\t# Recv error: {}".format(e))
            return
    else:
        packet = s.recvfrom(RECV_SIZE)
        packet = packet[0]

    ip_header = packet[0:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    ihl = version_ihl & 0xF

    iph_length = ihl * 4

    protocol = iph[6]
    # TCP only
    if protocol != 6:
        return

    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])
    # filter by ip
    if sip is not None and s_addr != sip:
        return
    if d_addr != hostip:
        return

    tcp_header = packet[iph_length:iph_length+20]

    tcph = struct.unpack('!HHLLBBHHH', tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]

    # filter by port
    if sport is not None and source_port != sport:
        return
    if hport is not None and dest_port != hport:
        return

    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4

    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    data = packet[h_size:]

    return d_addr, dest_port, s_addr, source_port, data, data_size


def get_cfg_path():
    if getattr(sys, 'frozen', False):
        bdir = os.path.dirname(sys.executable)
    else:
        bdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bdir, CFG_FNAME)


def load_config():
    cfg_path = get_cfg_path()
    sip = sport = hostip = hport = None
    with open(cfg_path) as f:
        data = yaml.load(f)
        if 'logger' in data:
            logconfig.dictConfig(data['logger'])
        if 'service' in data:
            adata = data['service']
            if adata is not None:
                hostip = adata.get('hostip')
                hport = adata.get('hport')
                sip = adata.get('sip')
                sport = adata.get('sport')
    return hostip, hport, sip, sport


hostip, hport, sip, sport = load_config()


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
        s = prepare_sniff(hostip)
        while rc != win32event.WAIT_OBJECT_0:
            try:
                main(s, hostip, hport, sip, sport)
            except Exception, e:
                logging.error("Service error: {}".format(e))
                break
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1)
        log_footer()
        servicemanager.LogInfoMsg("Service is finished.")


@click.group()
def test_dummy():
    pass


def log_header():
    logging.critical("\t# =========== Start connection monitoring ===========")
    cfg_path = get_cfg_path()
    logging.critical("\t# Config file: '{}', hostip: {}, hport: {}, sip: {},"
                     " sport: {}".format(cfg_path, hostip, hport, sip, sport))


def log_footer():
    logging.critical("\t# =========== Finish connection monitoring ===========")


def local_pinfo_by_addr(sip, sport):
    for con in psutil.net_connections():
        if con.status != 'ESTABLISHED':
            continue

        pid = con.pid
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            # logging.debug("\t# No such process: {}".format(pid))
            continue

        try:
            exe = proc.exe()
        except:
            # logging.debug("\t# Fail to get executable for pid: {}".format(pid))
            continue

        ppid = proc.ppid()
        try:
            pname = psutil.Process(ppid).name() if ppid is not None else None
        except psutil.NoSuchProcess:
            pname = "_destroyed_"
        name = proc.name()
        username = proc.username()
        ctime = datetime.fromtimestamp(proc.create_time())

        _sip, _sport = None, None
        if len(con.laddr) == 2:
            _sip, _sport = con.laddr
        if _sip == sip and _sport == sport:
            return name, pname, exe, username, ctime


def main(s, hostip, hport, sip, sport):
    res = sniff(s, hostip, hport, sip, sport)
    if res is None:
        return
    _hostip, _hport, _sip, _sport, data, datasize = res
    if datasize <= 1:
        return
    pinfo = local_pinfo_by_addr(_sip, _sport)
    if pinfo is not None:
        name, pname, exe, username, ctime = pinfo
    else:
        name, pname, exe, username, ctime = \
            None, None, None, None, None
    logging.info("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".\
                    format(_sip, _sport, _hostip, _hport, name, exe, pname,
                           username, ctime, data.encode('string-escape')))


@click.command()
@click.argument("hostip")
@click.option("--hport", type=int, help="target host port")
@click.option("--sip", help="target source ip")
@click.option("--sport", type=int, help="target source port")
def test(hostip, hport, sip, sport):
    log_header()
    s = prepare_sniff(hostip)
    while True:
        main(s, hostip, hport, sip, sport)

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
