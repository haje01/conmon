# conmon

로컬 프로세스의 모든 접속 정보를 모니터링한다.

## 설치

[릴리즈](https://github.com/haje01/conmon/releases) 에서 최신 배포본(.zip 파일)을 받고 압축 해제


## 도움말

    conmon.exe --help
    Usage: conmon.exe [OPTIONS]

    Options:
      --lip TEXT       target local ip
      --lport INTEGER  target local port
      --rip TEXT       target remote ip
      --rport INTEGER  target remote port
      --help           Show this message and exit.


## 사용 예

다음과 같이 실행하면 로컬 프로세스의 모든 네트워크 접속을 기록한다:

    common.exe

예를 들어 IP 주소에 관계없이 모든 포트 3306에 접속을 모니터링 하려면:

    common.exe --rport 3306

127.0.0.1의 3306으로 접근하는 접속을 모니터링 하려면:

    common.exe --rip 127.0.0.1 --rport 3306

## 로그 예

접속 기록은 `log.txt` 파일로 남고, 지정된 크기(기본 10MB) 이상이 되면 로테이션된다. 최대 10개까지 로그파일이 남는다. 로그 파일 내용은 다음과 같다:

    2017-05-23 17:03:42 - CRITICAL: =========== Start connection monitoring ===========
    2017-05-23 17:03:42 - CRITICAL: lip: None, lport: None, rip: None, rport: 8000
    2017-05-23 17:03:45 - WARNING: First connection from C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54403), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54400), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
    2017-05-23 17:03:45 - INFO: pid: 8520, ppid: 4924, name: chrome.exe, pname: chrome.exe, username: WEBZEN\haje01, exe: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, ctime: 2017-05-23 16:56:51, connection: sconn(fd=-1, family=2, type=1, laddr=('127.0.0.1', 54401), raddr=('127.0.0.1', 8000), status='ESTABLISHED', pid=8520)
