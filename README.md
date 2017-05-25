# conmon

로컬 프로세스의 모든 접속 정보를 모니터링한다.

[릴리즈](https://github.com/haje01/conmon/releases)에서 최신의 파일(conmon.zip)을 받고, 압축 해제하여 사용한다.


## 설정 파일

기본 설정 파일 `config.yml`을 편집하여 사용한다. 설정 파일은 `conmon.py` 스크립트 파일, 또는 `conmon.exe` 실행 파일과 같은 폴더에 있어야 한다. 설정은 크게 로그 설정과 서비스 설정으로 나뉜다. 먼저 로그 설정을 보자.

### 로그 설정

설정 파일의 `logger:` 아래에 로그 관련 설정이 있다. 이것은 파이썬 logger 설정 형식으로, 아래와 같은 기본 값을 가진다.

    logger:
        version: 1

        formatters:
            simpleFormater:
                format: '%(asctime)s, %(message)s'
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

## 콘솔 테스트

간단히 콘솔 모드로 테스트해볼 수 있다.

### 도움말

    conmon.exe test --help
    Usage: conmon.exe [OPTIONS]

    Options:
      --lip TEXT       target local ip
      --lport INTEGER  target local port
      --rip TEXT       target remote ip
      --rport INTEGER  target remote port
      --help           Show this message and exit.

### 사용 예

다음과 같이 실행하면 로컬 프로세스의 모든 네트워크 접속을 기록한다:

    common.exe test

IP 주소에 관계없이 모든 포트 3306에 접속을 모니터링 하려면:

    common.exe test --rport 3306

127.0.0.1의 3306으로 접근하는 접속을 모니터링 하려면:

    common.exe test --rip 127.0.0.1 --rport 3306


## 서비스로 이용하기

### 서비스 설정

`config.yml` 파일의  `service:` 아래에 다음과 같은 필드를 설정할 수 있다. 필요한 필드의 주석을 제거하고 기입하자.

    service:
        # lip: target local ip
        # lport: target local port
        # rip: target remote ip
        # rport: target remote port


### 윈도우 서비스

자동 시작 서비스로 설치

    conmon.exe --startup=auto install

서비스 시작

    conmon.exe start

서비스 정지

    conmon.exe stop

서비스 제거

    conmon.exe remove


## 로그 예

접속 기록은 `log.txt` 파일로 남고, 지정된 크기(기본 10MB) 이상이 되면 로테이션된다. 최대 10개까지 로그파일이 남는다. 로그는 CSV 형식으로 남는다:

각 필드의 이름은 다음과 같다.

    일시, 프로세스ID, 부모 프로세스ID, 실행파일 이름, 부모 실행파일 이름, 유저 이름, 실행파일 경로, 프로세스 생성 시간, 소스 IP, 소스 PORT, 목적지 IP, 목적지 PORT,

아래는 샘플 로그이다.

    2017-05-25 14:22:43, 7940, 4924, chrome.exe, chrome.exe, WEBZEN\haje01, C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, 2017-05-25 13:58:07, 127.0.0.1, 56331, 127.0.0.1, 8000
    2017-05-25 14:22:44, 7940, 4924, chrome.exe, chrome.exe, WEBZEN\haje01, C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, 2017-05-25 13:58:07, 127.0.0.1, 56331, 127.0.0.1, 8000
    2017-05-25 14:22:45, 7940, 4924, chrome.exe, chrome.exe, WEBZEN\haje01, C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, 2017-05-25 13:58:07, 127.0.0.1, 56331, 127.0.0.1, 8000
    2017-05-25 14:22:46, 7940, 4924, chrome.exe, chrome.exe, WEBZEN\haje01, C:\Program Files (x86)\Google\Chrome\Application\chrome.exe, 2017-05-25 13:58:07, 127.0.0.1, 56331, 127.0.0.1, 8000


## 변경 이력

- v0.1.0 - 최초 버전

- v0.1.1 - 윈도우 서비스화, CSV 형식 로그
