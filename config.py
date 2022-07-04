class Config:
    DbFile = "data.db"
    plugList = [
        {
            "name": "php_code_execute",
            "title": "自定义代码执行",
            "class": "CodeExecute",
            "logo": "resources/images/logo.png"
        },
        {
            "name": "msf",
            "title": "msf上线",
            "class": "MSF",
            "logo": "logo.png"
        },
    ]
    defaultHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
