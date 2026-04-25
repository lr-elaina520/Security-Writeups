这是文件上传类型的漏洞日志
编号      日期               题目                平台                介绍
 1    2026/4/25   [GXYCTF2019]BabyUpload      BUUCTF          php加apache的网站,易得知这个开发者使用正则表达式屏蔽了ph有关的字段，因为他是apche的网站，所以就想到上传.htaccess文件修改配置，把inc文件当
                                                              成php执行，把content-type换成image/jepg之后，成功。然后就是上传恶意文件，改名字文aaa.inc，content-type改为imag/jepg，失败，猜测他会
                                                              检查文件内容如：出现<? 之类的会过滤，或者他会检查文件幻数头，之后看了源码，确实是检查<?，所以使用<script language='php'>即可成功


 2    2026/4/25      [SUCTF 2019]CheckIn      BUUCTF          与编号1相似，他加了一个检查文件幻数头，并且禁止上传.htaccess文件和ph相关的文件，我尝试了使用\x00绕过（aa.php\x00.jepg），很显然没用，因为
                                                              是正则表达筛选的，之后随机上传一个普通文件，看到了那个目录中原本就有一个index.php文件，所以可以上传.user.ini文件，让所有php文件运行时先运行
                                                              同目录的我的恶意文件real.jepg，成功
                                                              
