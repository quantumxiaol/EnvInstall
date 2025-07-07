# Net

在服务器上部署代理服务，加速Github访问。

## V2ray

### 服务端部署

[V2ray](https://github.com/233boy/v2ray)

    bash <(wget -qO- -o- https://git.io/v2ray.sh)

### 客户端解压使用

没有root权限，解压使用。

[V2ray Client](https://github.com/v2ray/v2ray-core)

    wget https://github.com/v2ray/v2ray-core/releases/download/v4.28.2/v2ray-linux-64.zip

    unzip v2ray-linux-64.zip 

    cd /home/username/v2rayClient

    ./v2ray

    nohup ./v2ray -config config.json > v2ray.log 2>&1 &

### 客户端部署

需要root权限

创建用户v2ray

    sudo useradd -r -m -s /usr/sbin/nologin v2ray

    sudo mkdir -p /home/v2ray/v2ray
    sudo chown -R v2ray:v2ray /home/v2ray/v2ray/
    sudo chmod -R 755 /home/v2ray/v2ray/

    sudo -u v2ray -H sh -c "cd ~ && wget https://github.com/v2ray/v2ray-core/releases/download/v4.28.2/v2ray-linux-64.zip"

    sudo -u v2ray -H sh -c "unzip ~/v2ray-linux-64.zip -d ~/v2ray"

这会在 /home/v2ray/v2ray/ 目录下解压出 V2Ray 的相关文件。接着在 /home/v2ray/v2ray/ 目录下创建或编辑 config.json 文件。

    sudo -u v2ray nano /home/v2ray/v2ray/config.json

### 客户端配置

    协议 (protocol)         = 
    地址 (address)          = 
    端口 (port)             = 
    用户ID (id)             = 
    传输协议 (network)      = 
    伪装域名 (host)         = 
    路径 (path)             = 
    传输层安全 (TLS)        = 

```json
  "inbounds": [
    {
      "port": 1080,
      "listen": "127.0.0.1",
      "protocol": "socks",
      "tag": "socks-inbound",
      "settings": {
        "auth": "noauth",
        "udp": false,
        "ip": "127.0.0.1"
      },
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls"]
      }
    },
    {
      "port": 7890, // 新增的 HTTP 代理端口
      "listen": "127.0.0.1",
      "protocol": "http",
      "tag": "http-inbound",
      "settings": {}
    }
  ],

```


```json
"outbounds": [
    {
    "protocol": "vmess",
    "settings": {
        "vnext": [
        {
            "address": "",
            "port": 443,
            "users": [
            {
                "id": "",
                "alterId": 0,
                "security": "auto"
            }
            ]
        }
        ]
    },
    "streamSettings": {
        "network": "ws",
        "security": "tls",
        "tlsSettings": {
        "allowInsecure": false
        },
        "wsSettings": {
        "path": "/",
        "headers": {
            "Host": ""
        }
        }
    },
    "tag": "proxy"
    },
    {
    "protocol": "freedom",
    "settings": {},
    "tag": "direct"
    }
],
```

### 创建并配置 systemd 服务

    sudo nano /etc/systemd/system/v2ray.service

创建一个新的 systemd 服务文件 /etc/systemd/system/v2ray.service，内容如下：

    [Unit]
    Description=V2Ray Service
    After=network.target nss-lookup.target

    [Service]
    User=v2ray
    Group=v2ray
    Type=simple
    WorkingDirectory=/home/v2ray/v2ray
    ExecStart=/home/v2ray/v2ray/v2ray -config /home/v2ray/v2ray/config.json
    Restart=on-failure
    RestartSec=5s
    LimitNOFILE=infinity

    [Install]
    WantedBy=multi-user.target

启动服务

    sudo systemctl daemon-reload
    sudo systemctl enable v2ray
    sudo systemctl start v2ray
    sudo systemctl status v2ray

停止服务

    sudo systemctl stop v2ray

### 工具使用

可以通过环境变量HTTP_PROXY和HTTPS_PROXY设置代理

在~/bashrc中添加

    export HTTP_PROXY=http://127.0.0.1:7890
    export HTTPS_PROXY=https://127.0.0.1:7890

#### curl使用

    curl --socks5://127.0.0.1:1080 https://www.google.com
    curl --socks5-hostname://127.0.0.1:1080 https://www.google.com

    curl -x http://127.0.0.1:7890 https://www.google.com
    curl --proxy http://127.0.0.1:7890 https://www.google.com

    --socks5-hostname则是DNS解析也交给代理服务器执行
    

#### Git使用

Git 不直接支持 SOCKS5 代理，但可以通过一些工具（如 proxychains）来使用代理

全局使用代理，不建议，因为我们自己的gitlab不需要代理

    git config --global http.proxy 'http://127.0.0.1:7890'
    git config --global https.proxy 'http://127.0.0.1:7890'

特定仓库使用代理

    git config --local http.proxy 'http://127.0.0.1:7890'
    git config --local https.proxy 'http://127.0.0.1:7890'

单次git clone 使用代理

    git -c http.proxy="http://127.0.0.1:7890" -c https.proxy="http://127.0.0.1:7890" clone https://github.com/example/repo.git

#### wget使用

    wget -e use_proxy=yes -e http_proxy=127.0.0.1:7890 -e https_proxy=127.0.0.1:7890 https://example.com/file.tar.gz

wget 不原生支持 SOCKS5，所以需要用 proxychains 来强制它走 SOCKS5，

对于长期使用，创建 ~/.wgetrc

    use_proxy = on
    http_proxy = http://127.0.0.1:7890
    https_proxy = http://127.0.0.1:7890
    ftp_proxy = http://127.0.0.1:7890

#### pip下载

pip下载慢可以指定镜像，但有时需要从GitHub的源码安装。

pip默认使用http代理，使用--proxy指定代理ip，your-proxy-address为本机127.0.0.1，port默认7890（v2ray默认端口）

    pip install git+https://github.com/username/repository.git --proxy http://your-proxy-address:port

使用socks5代理，可能需要pysocks库，先执行`pip install pysocks`

    pip install git+https://github.com/username/repository.git --proxy socks5h://your-proxy-address:port
