
//error_reporting(0);
$sockID = base64_decode('__SOCKID__');
$forwardData = base64_decode('__DATA__');

$key = $_SESSION['key'];
$status = $_SESSION["status_$sockID"];

$data = array();
if (!$status) {
    $data["status"] = false;
    $data["data"] = "the socket have been closed.";
}

if ($forwardData) {
    $_SESSION["write_$sockID"] .= $forwardData;
    //header("Connection: Keep-Alive");
    $data["status"] = true;
}
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
