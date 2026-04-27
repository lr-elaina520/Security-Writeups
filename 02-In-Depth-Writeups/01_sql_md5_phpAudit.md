时间：2026/04/27      题目：[GXYCTF2019]BabySQli    平台：BUUCTF
目标：对漏洞进行分析和破解，以及总结我遇到的问题
<img width="390" height="267" alt="image" src="https://github.com/user-attachments/assets/d630250c-1757-4f75-bbb0-ef4f256c3fae" />
如上图中可知是个登录注册页面，思路如下：
攻击过程：
  1、先简单的' or 1=1# ，结果一直无响应，最后connetion reset，怀疑是前端服务器的WAF机制过滤了or，1=1之类的，所以/*!or*/ /*!1=1*/成功绕过WAF，但是后端明显检测到并过滤了'or'，之后试过了同样过滤'(' ')'和
  '='等
  2、想绕过过滤，尝试o/**/r，或者双写oorr，或者使用perpare hh from concat('s','elect', ' * from `1s4` ')之类的，结果无用，之后简单的试了一下大小写，结果成功绕过，猜测后端正则表达式没
  有管大小写，输入账号' /*!OR*/ /*!"23"*/#,密码乱输入，成功绕过，结果如下图
  <img width="250" height="140" alt="image" src="https://github.com/user-attachments/assets/446e4f1e-e8be-4047-8611-24a3ff0c962b" />
  看出来账号名name成功注入，但是password失败，说明他的后端并不是这样select * from table wherer name='...' and pwd='...' 
  猜测他是where name='...' 就行，然后用我的上传的password参数与sql查询结果相比较，如md5（$_POST['pw']）==查询结果中的pwd。
  先假设他是弱类型比较，并且他的查询结果中的pwd是0e234555之类的科学计数法结构或者是以数字开头的字符串，这样就可以使用经典的QNKCDZO之类的破解，但是无用
  3、查看github源码，重要字段如下图：
  <img width="777" height="979" alt="image" src="https://github.com/user-attachments/assets/ad7bea5e-e78a-4e52-a075-a7097f9f5f34" />
  可以看出和我猜测基本一致，只是对方的password是cd开头的，弱类型也无法绕过
  4、使用union方法，在账号名处输入asa' /*!union*/ /*!select 1,2,3*/#这样确认有几列（可以得知是3列），查看源码可知name必须是admin，所以尝试得到结果asa' /*!union*/ /*!select 1,'admin',3*/成功注入账号名，
  之后猜测3的地方是password的那一列，所以随机取一个字符串，我是用11111进行md5加密得到b0baee9d279d34fa1dfd71aadb908c3f，
  然后上传账号为asa' /*!union*/ /*!select 1,'admin','b0baee9d279d34fa1dfd71aadb908c3f'*/#，最后在密码处填写11111，成功
攻击成功原因：
    使用asa' union select 1，2，3结构作为账号名参数，后端查询时候发现name为asa的不存在，所以结果只有一行，就是union之后的1（id），2（name），3（psswd）.
    当传入asa' /*!union*/ /*!select 1,'admin','b0baee9d279d34fa1dfd71aadb908c3f'*/#时候，结果只有一行：1，admin，b0baee9d279d34fa1dfd71aadb908c3f
    然后结果中的admin成功绕过账号名，之后第三列b0b......与上传的参数md5('11111')弱类型比较为True，所以得到结果
总结：不能只局限于自己的认知，不能看到账号密码就带入后端只能select * from table wherer name='...' and pwd='...' ，它还可以只比较name，然后用查询结果继续比较，
  并且还有一种可能，他先是select * from table wherer name='...'之后得到name，然后select _POST['pwd'] from name；
之后遇到只比较一种的，可以使用union来‘伪造’结果
