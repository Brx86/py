# Aya的小爬虫合集

## 注意事项：

   - 合理使用，请勿滥用，如有后果概不负责
   - 移除了代理设置，个人使用请勿过于频繁（main.py一分钟不要运行超过一次），如果ip被B站拉黑请等待十分钟再次尝试

1. ## drawFans

   ### 简介：爬取B站用户粉丝并绘制饼图

   #### 环境需求：

   python >= 3.6

   #### 第三方库：

   requests, threadpool, pyecharts

   #### 使用方法：

   ```
   python main.py <UID>
   python calc.py <UID>
   
   # 例如：
   # 爬取共青团中央最近250个粉丝的用户数据，保存到"共青团中央/fans.csv"，可用excel等表格软件打开
   python main.py 20165629
   # 处理csv，计算并绘制饼图，保存到"共青团中央/pie.html"，可用浏览器打开
   python calc.py 20165629
   ```

   结果示例：https://note.aya1.top/bili/tuan

   

2. ## dynamicPic

   ### 简介：爬取B站用户动态的全部图片

   #### 环境需求：

   python >= 3.6

   #### 第三方库：

   requests, threadpool

   #### 使用方法：

   在当前文件夹执行`python main.py`或直接双击运行main.py，按照提示操作

   **例如：**

   爬取用户“小笼包纸酱”的全部动态, 将其中的图片链接保存到"2272909.txt"

   读取txt，使用多线程下载图片，保存到"2272909"文件夹下

   ```
   请输入需要爬取的用户UID: 2272909
   爬取链接后是否下载? (y/n) y
   已爬取第1页，下一页offset为464180235493025698
   已爬取第2页，下一页offset为420773096973814014
   ......
   共32页，爬取完成！
   总共有889张图片
   100.00%[==================================================>] 889 of 889
   全部图片下载完成，用时45.60秒！
   按回车键退出...
   ```

   

3. ## columnPic

   ### 简介：爬取B站单个专栏的图片或指定用户的全部专栏的图片

   #### 环境需求：

   python >= 3.6

   #### 第三方库：

   requests, asyncio, aiohttp

   #### 使用方法：

   在当前文件夹执行`python main.py`或直接双击运行main.py，按照提示操作

   **例如：**

   爬取用户“苏赛Marcus”的全部专栏, 将其中的图片链接保存到"uid13356120.txt"

   读取txt，使用异步下载图片，保存到"uid13356120"文件夹下

   ```
   请选择爬取内容(输入1/2): 
      1.指定用户的全部专栏图片
      2.指定单个专栏的全部图片
   1
   请输入需要爬取的用户uid: 13356120
   爬取链接后是否下载? (y/n) y
   正在处理用户“苏赛Marcus”...
   正在获取专栏列表 1/5...
   正在获取专栏列表 2/5...
   正在获取专栏列表 3/5...
   正在获取专栏列表 4/5...
   正在获取专栏列表 5/5...
   共有141篇专栏!
   正在处理cv13274976: [#118 Twitter上每日更新的古明地姐妹]
   正在处理cv13225874: [#117 Twitter上每日更新的古明地姐妹]
   正在处理cv13175074: [#116 Twitter上每日更新的古明地姐妹]
   正在处理cv13134319: [#115 Twitter上每日更新的古明地姐妹]
   ......
   总共有2437张图片！
   100.00%[==================================================>] 2437 of 2437
   全部图片下载完成，用时342.15秒！
   按回车键退出...
   ```

