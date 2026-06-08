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
