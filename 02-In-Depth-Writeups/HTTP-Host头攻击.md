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

  
第三关：
