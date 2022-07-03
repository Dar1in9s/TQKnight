
//error_reporting(0);
$sockID = base64_decode('__SOCKID__');

$key = $_SESSION['key'];
$status = $_SESSION["status_$sockID"];

$data = array();

if (!$status) {
    $data["status"] = false;
    $data["data"] = "the socket have been closed.";
} else {
    $data["status"] = true;
    $data["data"] = base64_encode($_SESSION["read_$sockID"]);
    $_SESSION["read_$sockID"] = "";
    //header("Connection: Keep-Alive");
}
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
