这是我创建这个git仓库之前做的未记录的一些安全方面的漏洞记录
以下是BUFUCTF里面的题目记录
1、[极客大挑战 2019]EasySQL，  简单的sql注入，答案是' /*!or*/ /*!1=1*/#，值得注意的是要使用/*!*/结构绕过前端服务器的WAF，否则会connection reset
2、[极客大挑战 2019]Havefun，  使用f12检查即可成功看到php代码，只用上传cat=dog的参数就成功了，值得注意的是有个echo $cat，可能存在xss攻击
3、[ACTF2020 新生赛]Include,  一眼就是php的文件包含漏洞，后端大概是这样的include（参数），所以/?file=php://filter/read=convert.base64-encode/resource=flag.php
4、[HCTF 2018]WarmUp,  鼠标右键检查去了source.php，看到源码，可知上传file参数，之后会include，但是他有白名单机制，只可以source.php或者hint.php，结合代码可以用？绕过，答案：source.php?file=hint.php?/../../../../ffffllllaaaagggg, 为了绕过WAF，要把../编码为%2e%2e%2f
5、[ACTF2020 新生赛]Exec，  网站叫我ping，我直接给一段ip;ls得知可以运行命令行，这样可以直接找到flag
6、[GXYCTF2019]Ping Ping Ping，  和上面那个类似，只是这个对空格和{}做了过滤，我先试用${IFS}当作空格，但是{}也被过滤，之后用$IFS$9，$9空参数，成功
7、[SUCTF 2019]EasySQL，  使用' or 1=1他会显示nonono，再加上输入1有Array ( [0] => 1 )，之后猜测他是select POST[] form 目标，上传*,1 成功（上传*失败）
8、[极客大挑战 2019]LoveSQL，  依旧是' or 1=1#尝试成功，回显账号名和密码，使用order by加上union select得知显示的是表的第二三列，之后就是联合注入看数据库了
9、[极客大挑战 2019]Secret File，  使用右键检查源码得到路径，进入路径，又有按钮，burt suite抓包得到目标路径，访问得到flag
10、
