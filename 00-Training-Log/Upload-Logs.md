这是文件上传类型的漏洞日志
编号      日期               题目                平台                介绍
 1    2026/4/25   [GXYCTF2019]BabyUpload      BUUCTF          php加apache的网站,易得知这个开发者使用正则表达式屏蔽了ph有关的字段，因为他是apche的网站，所以就想到上传.htaccess文件修改配置，把inc文件当
                                                              成php执行，把content-type换成image/jepg之后，成功。然后就是上传恶意文件，改名字文aaa.inc，content-type改为imag/jepg，失败，猜测他会
                                                              检查文件内容如：出现<? 之类的会过滤，或者他会检查文件幻数头，之后看了源码，确实是检查<?，所以使用<script language='php'>即可成功


 2    2026/4/25      [SUCTF 2019]CheckIn      BUUCTF                  
