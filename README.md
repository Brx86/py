# 小爬虫合集

1. ## drawFans

   ### 简介：爬取B站用户粉丝并绘制饼图

   #### 环境需求：

   python>=3.6

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
   
   #### 注意事项：
   
   1. 合理使用，请勿滥用，如有后果概不负责
   2. 移除了代理设置，个人使用请勿过于频繁（main.py一分钟不要运行超过一次），如果ip被B站拉黑请等待十分钟再次尝试
   
   

