# conmon

네트워크 패킷을 모니터링한다.

[릴리즈](https://github.com/haje01/conmon/releases)에서 최신의 배포 파일(conmon.zip)을 받고, 압축 해제하여 사용한다.


## 설정 파일

제공되는 설정 파일 `config.yml`을 환경에 맞게 편집한다. 설정 파일은 `conmon.exe` 실행 파일(배포 파일을 사용하는 경우) 또는 `conmon.py` 스크립트 파일(파이썬 스크립트로 실행하는 경우)과 같은 폴더에 있어야 한다. 설정은 크게 로그 설정과 서비스 설정으로 나뉜다. 먼저 로그 설정을 보자.

### 로그 설정

설정 파일의 `logger:` 아래에 로그 관련 설정이 있다. 이것은 파이썬 logger 설정 형식으로, 아래와 같은 기본 값을 가진다.

    logger:
        version: 1

        formatters:
            simpleFormater:
                format: '%(asctime)s%(message)s'
                datefmt: '%Y-%m-%d %H:%M:%S'

        handlers:
            console:
                class: logging.StreamHandler
                formatter: simpleFormater
                level: DEBUG
                stream: ext://sys.stdout
            file:
                class : logging.handlers.RotatingFileHandler
                formatter: simpleFormater
                level: DEBUG
                filename: C:\conmon\log.txt
                maxBytes: 10485760
                backupCount: 10

        root:
            level: DEBUG
            handlers: [console, file]

일반적으로 아래와 같은 필드를 필요에 맞게 수정하면 될 것이다.

`logger:handlers:console:level` 콘솔 로그의 레벨

`logger:handlers:file:level` 파일 로그의 레벨

`logger:handlers:file:filename` 파일 로그의 경로. 절대 경로로 기입한다.

`logger:handlers:file:maxBytes` 파일 로그의 크기. 이 크기 이상이면 로테이션 된다.

`logger:handlers:file:backupCount` 파일 로그의 로테이션 갯수.

위의 경우 로그 파일은 10MB 이상이 되면 로테이션되고, 최대 10개까지 로그 파일이 남는다.


## 콘솔 테스트

콘솔 모드로 간단히 테스트해볼 수 있다.

### 사용 예

다음과 같이 실행하면 호스트 127.0.0.1에 대한 로컬 프로세스의 모든 네트워크 접속을 기록한다:

    common.exe test 127.0.0.1

포트 3306에 접속을 모니터링 하려면:

    common.exe test 127.0.0.1 --rport 3306

### 도움말 보기

    conmon.exe test --help
    Usage: conmon.py test [OPTIONS] HOSTIP

    Options:
    --hport INTEGER  target host port
    --sip TEXT       target source ip
    --sport INTEGER  target source port
    --help           Show this message and exit.


## 로그 예

설정 파일에서 지정한 로그 파일에 접속 기록이 TSV 형식으로 남는다. 각 필드의 의미는 다음과 같다.

    일시, 소스 IP, 소스 PORT, 목적지 IP, 목적지 PORT, 실행파일 이름, 실핼파일 경로, 부모 실행파일 이름, 유저 이름, 프로세스 생성 시간, 메시지 내용

아래는 8000번 포트 접속 모니터링의 샘플 로그이다.
2017-05-26 16:20:54     127.0.0.1       62049   127.0.0.1       8000    chrome.exe      C:\Program F
iles (x86)\Google\Chrome\Application\chrome.exe explorer.exe    GROUP\haje01   2017-05-26 10:25:40
GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgr
ade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,ap
plication/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch, br\r\nAccept-Langu
age: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4\r\n\r\n

## 서비스로 이용하기

### 서비스 설정

설정 파일의 `service:` 아래에 다음과 같은 필드를 설정할 수 있다. 필요한 필드의 주석을 제거하고 기입하자.

    service:
        hostip: target host ip (required)
        # hport: target host port
        # lip: target local ip
        # lport: target local port
        # ifip: target interface ip, default: first interface ip


### 서비스 관리

자동 시작 서비스로 설치

    conmon.exe --startup=auto install

서비스 시작

    conmon.exe start

서비스 정지

    conmon.exe stop

서비스 제거

    conmon.exe remove


## 변경 이력

- v0.1.2 - 패킷 캡쳐, TSV 형식 로그

- v0.1.1 - 윈도우 서비스화, CSV 형식 로그

- v0.1.0 - 최초 버전
