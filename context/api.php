<?php
// error_reporting(0); // 隐藏PHP的日志信息
try {
    $conn = new Redis();
    $conn->connect('YOUR_REDIS_IP', YOUR_REDIS_PORT);
    $conn->auth('YOUR_REDIS_PASSWORD');
    if ($conn->get(("report." . $_SERVER["REMOTE_ADDR"])) > 40) {
        $message = new message();
        $message->fail('"请求过于频繁"');
        echo $message->show();
        return;
    }
    $conn->incr("report." . $_SERVER["REMOTE_ADDR"]);
    $conn->expireAt("report." . $_SERVER["REMOTE_ADDR"], intval(time()) + 20);
} catch (Exception $e) {
    //echo $e;
}

class message
{
    private $code = 0;
    private $msg = "";

    public function ok($msg)
    {
        $this->code = 0;
        $this->msg = $msg;
    }

    public function fail($msg)
    {
        $this->code = 1;
        $this->msg = $msg;
    }

    public function custom($code, $msg)
    {
        $this->code = $code;
        $this->msg = $msg;
    }

    /**
     * @return int
     */
    public function getCode()
    {
        return $this->code;
    }

    /**
     * @return string
     */
    public function getMsg()
    {
        return $this->msg;
    }

    /**
     * @param int $code
     */
    public function setCode($code)
    {
        $this->code = $code;
    }

    /**
     * @param string $msg
     */
    public function setMsg($msg)
    {
        $this->msg = $msg;
    }

    public function show()
    {
        echo '{"code":"' . $this->getCode() . '","msg":' . $this->getMsg() . '}';
    }
}

function doQuery($sql)
{
    try {
        $message = new message();
        $conn = mysqli_connect("YOUR_MYSQL_IP", "YOUR_MYSQL_USERNAME", "YOUR_MYSQL_PASSWORD", "YOUR_MYSQL_DATABASE_NAME", 3306);
        mysqli_query($conn, "set names utf8");
        $retval = mysqli_query($conn, $sql);
        if (!$retval) {
            $message->fail('无法读取数据: ' . mysqli_error($conn));
        }
        $arr = array();
        while ($row = mysqli_fetch_array($retval, MYSQLI_ASSOC)) {
            array_push($arr, $row);
        }
        $rst = json_encode($arr, JSON_UNESCAPED_UNICODE);
        $rst = trim($rst);
        $message->ok($rst);
        echo $message->show();
    } catch (Exception $e) {
        $message->fail($e);
    }
}

$rst = (array)json_decode(file_get_contents('php://input'), true);
if ($rst["method"] == "getv6") {
    doQuery("SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 0 DAY) ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 1 DAY) ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 2 DAY) ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 3 DAY) ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 4 DAY) ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT id FROM tp WHERE date(intime) = date_sub(date(now()), INTERVAL 5 DAY) ) tt;");
}
if ($rst["method"] == "getn6") {
    doQuery("SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 0 DAY ) GROUP BY sourceIP ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 1 DAY ) GROUP BY sourceIP ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 2 DAY ) GROUP BY sourceIP ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 3 DAY ) GROUP BY sourceIP ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 4 DAY ) GROUP BY sourceIP ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT sourceIP, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 5 DAY ) GROUP BY sourceIP ) tt;");
}
if ($rst["method"] == "getp6") {
    doQuery("SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 0 DAY ) GROUP BY targetPort ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 1 DAY ) GROUP BY targetPort ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 2 DAY ) GROUP BY targetPort ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 3 DAY ) GROUP BY targetPort ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 4 DAY ) GROUP BY targetPort ) tt UNION ALL SELECT count(*) AS sec FROM ( SELECT targetPort, intime FROM tp WHERE date( intime )= date_sub( date( now()), INTERVAL 5 DAY ) GROUP BY targetPort ) tt;");
}
if ($rst["method"] == "getbef10") {
    doQuery("SELECT a.*,b.Description as service from (SELECT sourceIP,targetPort,flag,intime FROM TP order by intime desc limit 10) a left join `service-names-port-numbers` b on a.targetPort = b.`Port Number` order by intime desc");
}
if ($rst["method"] == "gettopip10") {
    doQuery("SELECT sourceIP ,count(1) as sec FROM TP GROUP BY sourceIP ORDER BY count( 1 ) DESC LIMIT 15");
}
if ($rst["method"] == "gettopport10") {
    doQuery("SELECT a.*,b.Description as service from (SELECT targetPort ,count(1) as sec FROM TP GROUP BY targetPort ORDER BY count( 1 ) DESC LIMIT 15) a left join `service-names-port-numbers` b on a.targetPort = b.`Port Number` and b.`Transport Protocol` = 'tcp' order by a.sec desc");
}
if ($rst["method"] == "gettotal") {
    doQuery("SELECT count(1) as sec FROM TP");
}
if ($rst["method"] == "getwarn") {
    doQuery("SELECT flag ,count(1) as sec FROM TP group by flag order by sec desc ");
}
if ($rst["method"] == "ipatttime") {
    doQuery(<<<EOF
    SELECT concat( concat( YEAR ( intime ), concat( "-", concat( MONTH ( intime ), "-" ) ), concat(DAY ( intime )," ")), HOUR ( intime )) as dt, count( 1 ) AS sec FROM tp GROUP BY YEAR ( intime ), MONTH ( intime ), DAY ( intime ), HOUR ( intime ) ORDER BY intime DESC limit 100
EOF
    );
}

