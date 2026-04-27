编号      日期                 题目               平台         介绍
 1     2026/4/27      [De1CTF 2019]SSRF Me      BUUCTF        此题只是单纯的考验代码审计加一点SSRF，可以得知我最终要对De1ta伪造三个参数，即sign，param，action，其中param是flag.txt,action是readscan,
                                                              sign是某个加密函数（param，action）（之后这个函数成为A），只要让sign合理即可成功攻击，
                                                              又在另一个页面可以得知可以上传param参数使得到A(param,'scan')的结果，又因为他的A函数里都是使用加号拼接param和'scan'之后加密，所以在这个
                                                              页面上传param=flag.txtread，这样就可以得到sign
                                                              最后把param，action和sign上传到第一个也买你De1ta就可以成功

