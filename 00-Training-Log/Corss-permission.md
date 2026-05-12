  日期                 题目                    平台                  介绍
2026/5/12       [MRCTF2020]PYWebsite         BUUCTF                 进入页面，重要信息就是提交授权码的输入框，可能存在sql注入，之后尝试，暂时没有办法，放弃sql注入
                                                                    直接get请求flag.php,页面显示只有购买了某个东西的ip和管理员本地ip才可以得到flag，所以使用burp发送请求前添加请求头：
                                                                            X-Forwarded-For:127.0.0.1
                                                                    成功        
