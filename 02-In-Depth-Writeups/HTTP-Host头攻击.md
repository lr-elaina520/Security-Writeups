日期：2026/8/12           web安全学院        HTTP Host header attacks

第一关：Basic password reset poisoning
  介绍：这个网站会有重置密码功能，其中输入账号名，会给目标的邮件发送链接，链接有一个token参数，只要此参数正确即可修改密码，意味着只需要得到其中的参数就可以成功越权
  1、抓到/forgot-password ，并发送至Repeat，注意，Repeat中的Host头可以说是摆设，他和DNS解析无关，因为真正的host目标是右上方的Target，所以在Repeat中修改Host头不会修改目标ip。
  将Host修改为自己的漏洞利用服务器的域名，这样正常网站会给目标账号发送邮件链接，链接的域名和Host一致（感觉和修改X-Forwarded-Host请求头有点像）
   <img width="1261" height="694" alt="image" src="https://github.com/user-attachments/assets/44d42010-8854-455d-bbdf-c390183f2d2b" />
     
   注意：csrf是摆设，他没有作用在这个实验中

   2、发送Repeat后在漏洞利用服务器中找到日志中的token，成功修改


第二关：Host header authentication bypass
  1、访问robots.txt页面可以知道目标页面是admin，访问admin得知要本地用户才可以成功
  2、可以尝试修改XXF等请求头为127.0.0.1（没有尝试过），这道题因为是和Host有关，所以操作和第一关一样，改Host为localhost即可成功绕过
  <img width="1264" height="552" alt="image" src="https://github.com/user-attachments/assets/01ee0da4-a724-4de5-80f1-3a9f180782c3" />

  
  成功

  
第三关：Web cache poisoning via ambiguous requests
  介绍：这一关利用页面缓存投毒和Host头的攻击
  1、访问，查看请求，发现可以有缓存，联想到缓存投毒，但是缓存投毒一般把Host作为缓存键，如果和之前一样改了Host头部，那投毒就没有意义，因为别人的Host和你的Host不同，miss
  2、尝试单独修改Host，发现他不和一二关一样，他会校验Host是否一致，所以修改Host无效
  3、尝试引入X-Forwarded-Host头，依旧无效
  4、尝试使用两个Host头，发现可以成功得到响应，当然要注意，后端校验时候是以前一个Host头为主，意味着前一个Host头部要正确，后一个可以随意，并且可以知道他的js路径拼接是按照后一个
    Host头拼接的：
    <img width="1212" height="640" alt="image" src="https://github.com/user-attachments/assets/6f38e6e0-0de6-4973-9a38-f00944a9a859" />


  5、尝试投毒，将第二个Host改为自己的恶意网站，但在这之前要看看缓存键是第一个Host还是第二个Host，还是两个一起，如果是第一个作为缓存键即可成功，
    提示；加上一个随机的参数去看缓存键是哪个Host，因为参数一般也是缓存键，这样相当于自己给自己弄一个特殊的通道自己来试试，防止其他的人访问同一个缓存之类的，导致缓存重置成别人的
    第一次：
    <img width="1217" height="655" alt="image" src="https://github.com/user-attachments/assets/e2e4b4a1-38a4-44a9-a918-f428857f0a14" />

    第二次（无第二个缓存键）：
    <img width="1037" height="598" alt="image" src="https://github.com/user-attachments/assets/ffb8d89b-91ff-4a97-a9a4-32a77f94e75a" />

    缓存命中hit，说明他是以第一个Host为缓存键的

  6、恶意网站搭建，并且将第二个Host改为自己的恶意网站，恶意网站是一个路径为/resources/js/tracking.js的js文件
  <img width="1007" height="549" alt="image" src="https://github.com/user-attachments/assets/489122cc-582a-40e3-8635-bd3baa1465f3" />

  7、一直在repeat发送，直到你构造的请求的响应为miss就证明你已经成功投毒了  
  
  
  
