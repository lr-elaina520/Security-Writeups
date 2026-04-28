编号      日期                 题目                    平台         介绍
 1     2026/4/27      [网鼎杯 2020 朱雀组]phpweb      BUUCTF        点开页面burp抓包，上传参数分别是file_get_contents和index.php，得到源码，可以看到源码屏蔽了system之类的带有恶意的代码注入，同时
                                                                   index.php代码定义了一个Test类，这个类有个__destruct方法，方法实现了运行函数的功能，这个destruct功能没有过滤system之类的，所以思路
                                                                   就是上传的参数是unserialize和一个序列化对象的字符串，字符串里面的成员变量是func=system，p=ls /或者find / -iname *flag*，成功


