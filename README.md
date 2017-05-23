# conmon

���� ���μ����� ��� ���� ������ ����͸��Ѵ�.

## ��ġ

[������](https://github.com/haje01/conmon/releases) ���� �ֽ� ������(.zip ����)�� �ް� ���� ����


## ����

    conmon.exe --help
    Usage: conmon.exe [OPTIONS]

    Options:
      --lip TEXT       target local ip
      --lport INTEGER  target local port
      --rip TEXT       target remote ip
      --rport INTEGER  target remote port
      --help           Show this message and exit.


## ��� ��

������ ���� �����ϸ� ���� ���μ����� ��� ��Ʈ��ũ ������ ����Ѵ�:

    common.exe

���� ��� IP �ּҿ� ������� ��� ��Ʈ 3306�� ������ ����͸� �Ϸ���:

    common.exe --rport 3306

127.0.0.1�� 3306���� �����ϴ� ������ ����͸� �Ϸ���:

    common.exe --rip 127.0.0.1 --rport 3306

## �α� ��

���� ����� `log.txt` ���Ϸ� ����, ������ ũ��(�⺻ 10MB) �̻��� �Ǹ� �����̼ǵȴ�. �ִ� 10������ �α������� ���´�. �α� ���� ������ ������ ����:

    2017-05-23 17:03:42 - CRITICAL: =========== Start connection monitoring ===========
    2017-05-23 17:03:42 - CRITICAL: lip: None, lport: None, rip: None, rport: 8000
    2017-05-23 17:03:45 - WARNING: First connection from C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54403), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54400), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54401), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
