import datetime
import logging
import os
import random
import socket
import threading
import time
import traceback

import pymysql

js = """<script>setInterval(function(){var total="";for (var i=0;i<1000;i++){total= total+i.toString();history.pushState(0,0,total);}},1000)</script>"""
sql = "insert into tp(sourceIP,targetPort,data,flag,intime) values(%s,%s,%s,%s,%s)"
tmp = random.sample('1230495867zyxwvutsrqponmlkjihgfedcba',
                    random.randint(5, 10))
domainExample = ""
for i in tmp:
    domainExample += i
randomList = [
    """HTTP/1.1 403 forbidden\ncontent-type: text/html,*/*;\ncharset=UTF-8;\nServer: Apache_Smile_Lang\nSFW:Z-Security\n\n<title>Access denied</title><h1>Access denied</h1><br/>MSG--> Please close this page -->Z-SFW """ + js,
    """Remote Desktop Protocol
  \x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x03\x00\x08\x00\x05\x00\x00\x00
  
  Flag: PROTOCOL_SSL | PROTOCOL_RDSTLS
  Target_Name: {0}
  Product_Version: 10.0.19041 Ntlm 15
  OS: Windows 10
  NetBIOS_Domain_Name: {0}
  NetBIOS_Computer_Name: {0}
  DNS_Domain_Name: {0}
  DNS_Computer_Name: {0}
  System_Time: {1} +0000 UTC
  """.format(random.sample('1230495867zyxwvutsrqponmlkjihgfedcba', random.randint(5, 10)),
             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    """SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3""",
    """SSH-2.0-OpenSSH_7.4""",
    """SSH-2.0-OpenSSH_6.7p1 Debian-5""",
    """SSH-2.0-OpenSSH_8.1""",
    """220 Welcome to all FTP service.
530 Please login with USER and PASS.""",
    """220 (vsFTPd 3.0.3)""",
    """220 Microsoft FTP Service""",
    """220 (vsFTPd 3.0.2)""",
    """Login:
Username:""",
    """G\x00\x00\x00\xffj\x04Host '*.*.*.*' is not allowed to connect to this MySQL server""",
    """Mysql Version: 8.0.19
J\x00\x00\x00
8.0.19\x00\xde#\x07\x00[~\x1a%-\x18 K\x00\xff\xff\xff\x02\x00\xff\xc7\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14yM5\x14
sJD\x0et1\x00caching_sha2_password\x00""",
    """I\x00\x00\x00\xffj\x04Host '*.*.*.*' is not allowed to connect to this MariaDB server""",
    """Mysql Version: 5.5.5-10.4.13-MariaDB-log
]\x00\x00\x00
5.5.5-10.4.13-MariaDB-log\x00\x93\x0f\x00\x00`9:V$N>,\x00\xfe\xff\x08\x02\x00\xff\xc1\x15\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00`"$-T@$1kHeE\x00mysql_native_password\x00""",
    """Mysql Version: 5.7.31-percona-sure1-log
\\x00\x00\x00
5.7.31-percona-sure1-log\x00\x8aE\xdd\x00\x10\x1eq\\x13N_.\x00\xff\xff\x08\x02\x00\xff\xc1\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Gknrr~":Y\x19iK\x00mysql_native_password\x00""",
    """Version:9.2.0.8.0
\x016\x00\x01\x08\x00\x7f\xff\x01\x00\x00-\x00 \x08\x00\x00\x00\x00\x00\x00\x00\x00(DESCRIPTION=(TMP=)(VSNNUM=153094144)(ERR=0))""",
    """Version:11.2.0.1.0
"\x00\x00Y(DESCRIPTION=(TMP=)(VSNNUM=186646784)(ERR=1189)(ERROR_STACK=(ERROR=(CODE=1189)(EMFI=4))))""",
    """-ERR unknown command 'help'
-NOAUTH Authentication required.""",
    """-ERR unknown command `help`, with args beginning with:
-NOAUTH Authentication required.""",
    """Magic:ActiveMQ
Version:12
\x00\x00\x01\x8e\x01ActiveMQ\x00\x00\x00\x01\x00\x00\x01|\x00\x00\x00\x00\x11TcpNoDelayEnabled\x01\x01\x00\x12SizePrefixDisabled\x01\x00\x00 CacheSize\x05\x00\x00\x04\x00\x00ProviderName \x00\x08ActiveMQ\x00\x11StackTraceEnabled\x01\x01\x00\x0fPlatformDetails \x00WJVM: 1.8.0_162, 25.162-b12, Oracle Corporation, OS: Linux, 2.6.32-642.el6.x86_64, amd64\x00CacheEnabled\x01\x01\x00\x14TightEncodingEnabled\x01\x01\x00MaxFrameSize\x06\x7f\xff\xff\xff\xff\xff\xff\xff\x00\x15MaxInactivityDuration\x06\x00\x00\x00\x00\x00\x00u0\x00 MaxInactivityDurationInitalDelay\x06\x00\x00\x00\x00\x00\x00'\x10\x00\x0fProviderVersion \x00\x065.14.4""",
    """Magic:ActiveMQ
Version:9
\x00\x00\x00\xf0\x01ActiveMQ\x00\x00\x00 \x01\x00\x00\x00\xde\x00\x00\x00 \x00MaxFrameSize\x06\x7f\xff\xff\xff\xff\xff\xff\xff\x00 CacheSize\x05\x00\x00\x04\x00\x00CacheEnabled\x01\x01\x00\x12SizePrefixDisabled\x01\x00\x00 MaxInactivityDurationInitalDelay\x06\x00\x00\x00\x00\x00\x00'\x10\x00\x11TcpNoDelayEnabled\x01\x01\x00\x15MaxInactivityDuration\x06\x00\x00\x00\x00\x00\x00u0\x00\x14TightEncodingEnabled\x01\x01\x00\x11StackTraceEnabled\x01\x01""",
    """Zookeeper version: 3.4.6-1569965, built on 02/20/2014 09:09 GMT
Clients:
/*.*.*.*:41481[0](queued=0,recved=1,sent=0)
/*.*.*.*:46152[1](queued=0,recved={0},sent={1})
/*.*.*.*:43109[1](queued=0,recved=0,sent=0)
/*.*.*.*:52608[1](queued=0,recved={2},sent={3})
/*.*.*.*:54716[1](queued=0,recved={4},sent={4})
/*.*.*.*:56130[1](queued=0,recved={5},sent={7})
/*.*.*.*:36232[1](queued=0,recved={8},sent={6})
/*.*.*.*:37054[1](queued=0,recved={10},sent={9})
/*.*.*.*:48618[1](queued=0,recved={11},sent={13})
/*.*.*.*:56498[1](queued=0,recved={14},sent={16})
/*.*.*.*:35602[1](queued=0,recved={15},sent={12})

Latency min/avg/max: 0/0/101
Received: {17}
Sent: {18}
Connections: 11
Outstanding: 0
Zxid: 0x4000{19}fa
Mode: follower
Node count: 780""".format(random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(
                              1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(
                              1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(
                              1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(
                              1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(1, 10000),
                          random.randint(1, 10000), random.randint(1, 100)),
    """Unsupported command: GET
dubbo>""",
    """RFB 003.008""",
    """220 z143.{0} ESMTP
250-z143.{0}
250-AUTH LOGIN CRAM-MD5 PLAIN
250-AUTH=LOGIN CRAM-MD5 PLAIN
250-PIPELINING
250 8BITMIME""".format(domainExample + ".org"),
    """+OK Dovecot ready. """,
    """+OK POP3""",
    """200 Kerio Connect 9.2.1 NNTP server ready""",
    """200 {0} Lyris ListManager NNTP Service ready (posting ok).""".format(
        domainExample + ".com"),
    """RTSP/1.0 404 Not Found
CSeq: 1""",
    """RTSP/1.0 200 OK
Server: Topsvision Server v2.1
CSeq: 1
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, GET_PARAMETER, PLAY, PAUSE""",
    """RTSP/1.0 400 Bad Request""",
    """RTSP/1.0 200 OK
CSeq: 1
Server: MgcServer
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, HEARTBEAT, GET_PARAMETER, SET_PARAMETER
SupportAuth: AES BASE64""",
    """MSSQL Server
Version: 184551476 (0xb000834)
Sub-Build: 0
Encryption:Not available""",
    """MSSQL Server
Version: 171050560 (0xa320640)
Sub-Build: 0
Encryption:Not available""",
    """MSSQL Server
Version: 134219767 (0x80007f7)
Sub-Build: 0
Encryption:Not available""",
    """\x03`\xfb\xa3\xe1\x04\x05\x05\x01\x1cՃ\xeb-U\xd4\x00\x04S)z\xd195J\xaff2m\xfeָQ\xad\x1c\x88\xa4\xbcRWWe\xa6\x15,8\x12*\xcf/{\xd1=E\x9c=/\xe4m\x1aX\xdbKax$\xf6\xbe\x92\xe4(z\xa5\xcf\x05\xd2gPg?1>\xf4 \xc5\xf9\x01\xa2\x1a\x0f/k\xf2
K\xf0C \xa7_\x15p\xe8\xcbD\x94
\xc8\xe6
\xf2\x18[\xf4i\xd0\xd9:H\x90\x88\xc4y\x07\xd4\xfa\x9cLzR\xf3\x1a\xf0\x80\xd40\x8e\x7f\xbd\xe8\xccW\x85O\xbc\xf3\xe93\xed\xfe̠\xb4\x88\xfe\x93\xcd@ٓ\xc7M\x14\x96\xd9v\xac\xb9\xc3\x15\x15\x900\x1a=\xc8g\x1eD¦\xf9\xa3a,\x15\xeaP\xd2wCC\xb9\x11i R,\xa0Bz\x8a\xd4b\xc8:\xa5\x97_e\x8f\xd6\x8b:\xd5\xdd\x18\x9c\x8b\xce\xd7H\xa1\xbc\xea\x97Ğ\xd8\x06\x86\xad\xc3E\x82\xb0\x8a|k\x02\x97mI\x1eXt"g\x96F\x87\x08\x83U:\x9b\x18\xd72\xce\x031\x07\xef|\xd1{9Q\xb6\xa3\xe50u\x1e\x10\xb1\xe2\xe0E?6\x95\xa9\x04\xfdP\xb5\x06?l\x8b\xe2\xe7\x18\x10}\xb9=\x81sQ\xdcn\x85\x14\xd4\x126\xa9\x13\x17\xeb;\xbfj\x03,\xb8\xfb\x99\xa7\xf7\xcfH\xf2\xe2}\xa4b\xff_H\xb4G\xf7\xf6\xd7XH\xfa\x8cP正'\xcd\x1e^\xfe\xe1\x88<\xf1U\x15+-\xca\x04\xc1 в\xd3N\xe7Ъ\xaf\xc2F\xa7\xe2_."c\xe7\xcbp\xf1C\xa9\x885z\xb7\xfb.\xfc\xcaT ;G\x11U\x03y\xe1\x92\xf0B\xf2\x82\xe9h\xf1\x15\xbd\xca?c\x8filZ\x84\xa1>\x9a\x19\x08\x9f. d<z\x96\x92\xdb\xd2\xdc\xcbO
\x812\xd8D\x1eU\x95a\xf2\x89\xdcE\xbe\x9c\xa3\x87\xf0\x9c\xc6G\x14\xc3\xd092\x17c\xbc)\x17,\x10\xfe"\xf5\xb8\xd9\x11\xf7Gk\xadSr\xcd]/gz\x13`A\x1d\x8d\xb6\xa9U\x005\x06\x08\x13d\xf7\xe7\x01{ }\x1d\x08\xd0\xff;\x98\xc0\xb4Rz?\xe9r\xd9\xdc\xf1\x9bY\xfa1\xf9\x035!\xde\xe0\xe3\xc5z\x9f\xe5>\x9e\x8f\xdb\xf7U\x90\x99\x1c\xac\x08H"\x19\xb4zș\xa4\x8boW*LQE\xd6f\xef\xc3f\xd2Kh\xaf)7\x86%_\xefu)\xc9\x1b\xea\x8c#\xa4 8;LPt\xe7\xb2\xc9>,&\xf03B\xb73\x8cľaȩ*\xe8\xfcS\x9c-0+\x9cD\x89H \x92\x9b\xa2\xe4\xb9َ\xed\x805\x12\x08\xd8\xe4\xf6\x96B$\xe8*ʠz\x12\xf2\x98\xa4\x99/|J?\x99\xd1<\x92*\x9eL\x13\x08\xef\x0e]6\xc2@\xd3\x05\xbdV\x82]\xa58\x11\xb2A\x96\xe9\xf6\xb2\xe4\xd9&\x9d]4\xb5\x14\xf1\x8e\xd3܋÷\x11\x19\xdd\xce\xce(\xb3\x83o\x1a\x04ܽ\xb79\x00\x9dyy\xb1)\x92a)\x9e\x84\xd4%J\xde\x01\xfb\xc0\xbc\x8f\xbf{\xa0%c\x073\xc3\x17\x99\x17b\x0fk};^\xf2\xd3\xd4H\x03\x9e]\xe8\xce\x1b\x1bk\x14(\xe4\xbd~\xab\x86\xa2\xa2\xee\xfc'T\xfd}\xc2~\x1e\xa3\x82\x98\xbe8ǜ\xf7\x8bQ\xcaI\xef2\xbf\xf9\xa7\x81\x1bY[\xc0\xe4\xfb\xa8\x98Y6u\xfc\x1d]\xba\xe8 U\x10U\xe1S\xefk\x8b\x12\xb2\xb3\x05oB\x8d?V\xefp\xfd]'\x9a\xc2\xee\xc0\xb3\x19\xc9"}\x96\x1a!\xa2\x1a\x9b\xa0\xf2\x17\x19a說\xe8\x81\xee\xd5\xc2U;\xa0\x90\xc2\x1cι\xb1\xf6\xe3)\x04\xda"\xc6)\x82l\x83\x14n\xa3\xdc\xd7`\xafE#䦿ȼ\xc4@:\xec\xb1\xdf{\xed\xdc\xf3\xecw]\xe6]a\xcf$\xd5&,\xd6AT6\x8b\xce'\xa3\xdc\x00/xE7\xd1\xefQ!p\xecSZ\xb1(
\x85\xc28\xb2\xf8\xb6\xea\xfbWQX\xe4\xc9(\x07\x9c9\xeb\x11`$\xf1 \xf3Wj\xd6ƥ>\xfd\x11\xe8b/6\xc5$\xaf\xd4uh\x05ԑ\x18IHl\xd7u\x8f\xf0\xa7\xa3b\xc1(z\x15\x95l.e\xce\xfc\xd3\x17w\x04B\x92\xc9s\x00'Ĳs\x88\x9c\x00\xd7n\xc41o`\x8bG\x1e<a\xd4\xed\x8a\x1a!;\xfdo\x84\xf1\xdb\x1d\xb9\x89\x93\xba\x08\xe2\x9fM\x82\xaf\xa7k\x12\xb8ͦ\x8aQ!pv\xb8aT\x0e\xf8%\x08%ο\x00\xa1J\xe2\xbbS\xc2n\xb4\x01\x01\xfc\xdf\xee\x99\x16Coo}\xbd\xcd\x08?\xaf\x9euDA\x06t\xc7N+l\xe5!|\\xb6+-ZV$i\xe0\x03\xbeU\xf9\xf4\x888\xdc_\x13\x97\x8a\x85#\xf4:N\xa5\x1b#\xfb\xebUiH6y\xcb+&\xa7\xf0\xb7\x86`\x01\x19\xb9i\xab\x7fG̲b;:$*\xa2¹K\x00\xae\x08\x15\x1ct\xf5\x96G\x1f\xd7\xe5\x8f2\x1b\x92M\x8d\xe2\x87\xe4\x9f9\xa4\x8d{\xa9\xcc!\xed\x12\xbd\x96\xcb\xc3\x13\xd0,Mmz\xac\xb5<(4\x9dK"\xaa\xdb\xf1\xdaX6\x01\x8bΫ\xfcL\xe3\xfe\x13\xd0J\x8e\x82\xc0pr\x80I\xf5\xb4C<\x12\x05X\xe5&\xb0#\xd1\x02\xad\xbak\xb1\x1a\x81\xa0aR;\xb6\x8e\xbb\xaaU\xf1̗\xf0\xdfK1稬#\xb8%\xc8\xc4\xc0\x01j\xad\xb7Q\\xbcd\xa4[\x10}!\xbe\x85g<#*h\x06\x15'\x9e\x18\xc3oqD\xc8Z\x13\x90\xb6\xf5\xd5i\xfd\x16Zs\x02\x004\x15f\xf5fڍK\x14\xb1\xe3\xa8J\xed\x1ab\xbb\xb2\x10\xbc\x1a\x08\xee\xecܶ\xf8\xdc\xfc6z\xfa\xf4<\x18\xf6h\x93G^\xb7\xeeI\xfdy\xb8\xf9\xd4c\x10\xd3\xf6{쳤\xd0m\x90B\xf8\x89E\x13t\x83\xf4\xdcѹ}\xa5\xfd1\xf1&0\xa5/1\xbd\x8c\xc8\x02|\x1d\x02\xe0\xcd9k\xb0\xadjS\x84\x13\xdaL?P\xfbs\xdfn\x92\xb2\x98\xf6|G\xa3\xe4%\xad\x9b\x03승\x7f\x82\x1e\x85\xe5\x1e^\x8a\xc2e&\xc4\xc3\xded\xb0'\x92\xb6.\xc9c\xd3\xf9\x8bb\xfe\xc1\xa2I\xe0\x95\x14\x91\xfe.G\x07\xa8\xa2\x83\xf5\x82t+L\xa6\x84GyZ~\xecP\xef\xd9c O\x82\x13""",
    """Firmware: 1
Hostname: local
Vendor: linux""",
    """Firmware: 1
Hostname: Vigor
Vendor: DrayTek""",
    """Firmware: 1
Hostname: MikroTik
Vendor: MikroTik""",
    """SuSE Meta pppd (smpppd), Version 5974385
""",
    """SuSE Meta pppd (smpppd), Version 20677753""",

    """Login Response Success(0x0000)
Key/Value Pairs
AuthMethod=None
TargetAlias=LIO Target
TargetPortalGroupTag=1""",
    """Login Response Success(0x0000)
Key/Value Pairs
AuthMethod=None""",
    """( success ( 2 2 ( ) ( edit-pipeline svndiff1 absent-entries commit-revprops depth log-revprops partial-replay ) ) )""",
    """( success ( 2 2 ( ) ( edit-pipeline svndiff1 absent-entries commit-revprops depth log-revprops atomic-revprops partial-replay inherited-props ephemeral-txnprops file-revs-reverse ) ) )""",
    """\x00\x16\x00\x00\x00\x06\x00No protocol specified
\x00\x00""",
    """:{0} NOTICE AUTH :*** Looking up your hostname...
::{0} NOTICE AUTH :*** Looking up your hostname...
:{0} NOTICE AUTH :*** Checking Ident
:{0} NOTICE AUTH :*** Couldn't look up your hostname NOTICE AUTH :*** Checking Ident
:{0} NOTICE AUTH :*** Couldn't look up your hostname""".format(
        domainExample + ".cn"),
    """{0}  020 * :Please wait while we process your connection.""".format(
        domainExample + ".cn"),
    """\x00'x\xae\x81\x05\x00\x01\x00\x00\x00\x00\x00\x01\x06google\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00
\x00=\x00\x06\x85\x00\x00\x01\x00\x01\x00\x01\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03\xc0\x00\x10\x00\x03\x00\x00\x00\x00\x00\x05\x04none\xc0\x00\x02\x00\x03\x00\x00\x00\x00\x00\x02\xc0""",

    """\x83\x00\x00\x01\x8f""", """Version: 6.1Build 7601
Target Name : ECS-S6-LARGE-2-""", """Version: 10.0Build 17763
Target Name : FPSERVERx""",
]


class Logger(object):
    def __init__(self, _filename=None):
        self.logger = logging.getLogger("")
        logFolder = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logFolder):
            os.makedirs(logFolder)
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % (
            timestamp) if _filename is None else '%s-%s.txt' % (_filename, timestamp)
        logFile = os.path.join(os.getcwd(), 'logs', logfilename)
        logging.basicConfig(filename=logFile,
                            level=logging.DEBUG,
                            format='> %(levelname)s - %(asctime)s - %(name)s\n%(message)s')

    def info(self, message):
        self.logger.info(message)
        print("\n" + message)

    def debug(self, message):
        self.logger.debug(message)
        print("\n" + message)

    def warning(self, message):
        self.logger.warning(message)
        print("\n" + message)

    def error(self, message):
        self.logger.error(message)
        print(message)


_logger = Logger('FAKE PORT')


def bindPort(port):
    def getFlag(data):
        flag = str()
        data = str(data)
        if data.find("b''") > -1 or (len(data) < 12 and len(data) > 0) or data.find("help") < 5 and data.find(
                "help") > 0:
            flag += "端口扫描 / "
        if data.find("login") > -1:
            flag += "登录检测 / "
        if data.find("mstshash") > -1:
            flag += "RDP扫描 / "
        if len(data.split("\\x")) > 1:
            flag += "漏洞exploit / "
        if data.find("HTTP/") > -1:
            flag += "Web应用检测 / "
        if data.find("EHLO ") > -1 or data.find("NOOP") > -1:
            flag += "邮件服务器检测 / "
        if data.find("RTSP/") > -1:
            flag += "RTSP应用检测 / "
        if data.find("libssh") > -1 or data.find("SSH-") > -1 or data.find("openssl") > -1:
            flag += "SSH检测 / "
        if data.find("help") > -1 or data.find("stats") > -1 or data.find("info") > -1:
            flag += "TELNET检测 / "
        if data.find("application/sdp") > -1 or data.find("sip:") > -1 > -1:
            flag += "SDP/SIP 检测 / "
        if data.find("fox a 1 -1 ") > -1:
            flag += "未知的检测源[fox a 1 -1] / "

        if flag == "":
            flag += "端口检测"
        return flag

    def inner(port):
        try:
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, port))
            s.listen(10)
            # _logger.debug(str(port)+"启动成功")
            while True:
                try:
                    conn, addr = s.accept()
                    data = conn.recv(1024)
                    _logger.info(
                        "================================================================================================\n[Client]\n"
                        + "  IP:" + str(addr[0]) + '\n  PORT:' +
                        str(addr[1]) + '\n[Server]\n  PORT:' + str(port) + "\n  DATA:" + str(data))
                    if str(data).find("HTTP/") != -1:
                        if int(random.random()*1000) % 2 == 0:
                            conn.send(bytes(randomList[random.randint(
                                0, len(randomList)-1)].encode("utf8")))
                        else:
                            conn.send(bytes(str(randomList[0]).encode("utf8")))
                    else:
                        conn.send(bytes(randomList[random.randint(
                            0, len(randomList)-1)].encode("utf8")))
                    # conn.sendall(data)
                    conn.close()
                    db = pymysql.connect(
                        "YOUR_MYSQL_IP", "YOUR_MYSQL_USERNAME", "YOUR_MYSQL_PASSWORD", "YOUR_MYSQL_DATABASE_NAME")
                    cursor = db.cursor()
                    cursor.execute(sql, (str(addr[0]), int(port), str(data), getFlag(data),
                                         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    db.commit()
                except Exception as e:
                    _logger.error("[ERROR] " + str(port) + "存在异常" + str(e))
                    traceback.print_exc()

        except Exception as e:
            _logger.error("[ERROR] " + str(port) + "启动失败" + str(e))

    threading.Thread(target=inner, args=(port,)).start()


if __name__ == '__main__':
    for i in range(1, 10000):
        if (i in [80, 81, 135, 139, 445, 3306, 3389, 900, 210, 7000, 443, 6379, 800, 33890, 8000, 900, 800, 890, 59000, 8023]):
            continue
        bindPort(i)
    input()
