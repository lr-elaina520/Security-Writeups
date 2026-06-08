  日期                 题目                    平台                  介绍
2026/5/12       [MRCTF2020]PYWebsite         BUUCTF                 进入页面，重要信息就是提交授权码的输入框，可能存在sql注入，之后尝试，暂时没有办法，放弃sql注入
                                                                    直接get请求flag.php,页面显示只有购买了某个东西的ip和管理员本地ip才可以得到flag，所以使用burp发送请求前添加请求头：
                                                                            X-Forwarded-For:127.0.0.1
                                                                    成功        



2026/6/8            文件路径遍历             Web安全学院              第一题：越权访问etc/passwd，点击产品信息同时抓包会抓到GET /image?filename=...的数据包改为
                                                                    filename=../../../etc/passwd成功
                                                                    第二题:也是filename=/etc/passwd，只是这个无法使用../遍历，但是它将提供的文件名视为相对于默认工作目录所以成功
                                                                    第三题：答案是filename=....//..././..././etc/passwd ，因为他会把../删除（没有递归删除），所以使用双写绕过
                                                                    第四题：答案是filename=..%252f..%252f..%252fetc/passwd，因为会先进行解码由于前端会进行一次解码后端会进行一次所以两次编码
                                                                    第五题：正常请求变为GET /image?filename=/var/www/images/52.jpg ，是因为要完整的路径不要相对路径所以改成
                                                                            filename=/var/www/images/../../../etc/passwd
                                                                    第六题：答案是filename=../../../etc/passwd%00.png ，因为有些在底层 C 语言风格的字符串处理中，%00被编码成\0，这是c中的字符串
                                                                            结尾所以在../../../etc/passwd%00.png中后面的.png会被忽略


2026/6/8            访问控制漏洞             Web安全学院              第一题：访问robots.txt得到目标路径：/administrator-panel，然后可以删除目标用户
                                                                    第二题：f12开发者工具，找到admin-llnib3路径，访问，删除目标
                                                                    第三题：访问/admin，没有权限。登录普通用户账号，得到cookie为Cookie: Admin=false; session=Wbc1WOFqu7CGNYuZ6yK9p17p3EOk6iqo，
                                                                            将Admin改为true访问/admin,成功
                                                                    第四题：提示中有roleid=2时候可以成功访问，然后bp抓包得到在更新账号的邮件的功能中会有一个302重定向的响应包发现响应中的roleid为1，
                                                                            所以上传请求：
                                                                            POST /my-account/change-email HTTP/2
                                                                            Host: 0acc001c04a3dbeb80259952003f0043.web-security-academy.net

                                                                            {"email":"admin1@normal-user.ne",
                                                                             "roleid": 2
                                                                            		}

                                                                            成功
                                                                     第五题：登录自己的账号，将id改为 /my-account?id=carlos  成功得到api
                                                                     第六题：找到目标用户发布的评论，得到他的uid，将accout里面的uid改成他的即可成功
                                                                     
                                                                            
    
