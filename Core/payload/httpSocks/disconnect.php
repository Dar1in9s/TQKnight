
error_reporting(0);
$key = $_SESSION['key'];
$sockID = base64_decode('__SOCKID__');
$data = array("status" => true);

if (isset($_SESSION["status_$sockID"]))
    $_SESSION["status_$sockID"] = false;
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
