import os, csv, time, requests, asyncio, aiohttp
from pyecharts import options as opts
from pyecharts.charts import Page, Pie


class Spyder:
    def __init__(self, mid):
        self.mid = str(mid)
        self.session = requests.Session()
        self.status = self.getName()

    def getName(self):
        userApi = f"https://api.bilibili.com/x/web-interface/card?mid={self.mid}"
        try:
            up = self.session.get(userApi).json()["data"]
            self.upName = up["card"]["name"]
            self.upFans = int(up["follower"])
        except:
            print("请勿频繁请求")
            return
        if self.upFans < 250:
            self.upPages = int(self.upFans) // 50 + 1
        else:
            self.upPages = 5

    def getFans(self, pn):
        print(f"正在获取列表 {pn+1}/{self.upPages}...")
        fansApi = (
            f"http://api.bilibili.com/x/relation/followers?vmid={self.mid}&pn={pn+1}"
        )
        return self.session.get(fansApi).json()["data"]["list"]

    async def getInfo(self, client, u):
        userApi = f"http://api.bilibili.com/x/space/acc/info?mid={u['mid']}&jsonp"
        r = await client.get(userApi)
        try:
            ui = await r.json()
            ui = ui["data"]
            print(f"UID: {u['mid']}\tLevel: {ui['level']}")
        except:
            print("请勿频繁请求")
            return
        with open(f"{self.mid}/{self.upName}.csv", "a+") as f:
            wCsv = csv.writer(f)
            wCsv.writerow(
                [
                    u["mid"],
                    u["mtime"],
                    u["uname"],
                    u["vip"]["vipType"],
                    ui["level"],
                    ui["sex"],
                    u["sign"].replace("\n", " "),
                ]
            )
        return 1

    def draw(self):
        sumUsers = 0
        lvList = [[f"lv{x}", 0] for x in range(7)]
        with open(f"{self.mid}/{self.upName}.csv", "r") as f:
            rCsv = csv.reader(f)
            for line in rCsv:
                if not line[4].isdigit():
                    continue
                lv = int(line[4])
                sumUsers += 1
                lvList[lv][1] += 1
        for u in range(7):
            lvList[u][1] = round(100 * lvList[u][1] / sumUsers, 2)
        tTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 30))
        pie = (
            Pie()
            .add("", lvList, radius=["30%", "70%"], center=["55%", "50%"])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{self.upName} 粉丝等级占比",
                    subtitle=f"最后更新于: {tTime}\n\n样本数: {sumUsers}/{self.upFans}\n\nUID: {self.mid}",
                    pos_left="15%",
                ),
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="30%", pos_left="15%"
                ),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
        )
        pie.render(f"{self.mid}/index.html")
        print("统计图已生成! ")

    async def main(self):
        uList = []
        if not os.path.exists(self.mid):
            os.mkdir(self.mid)
        with open(f"{self.mid}/{self.upName}.csv", "w+") as f:
            f.write("uid,mtime,uname,vipType,level,sex,sign\n")
        for i in range(self.upPages):
            uList.extend(self.getFans(i))
        async with aiohttp.ClientSession() as client:
            tasks = [self.getInfo(client, u) for u in uList]
            await asyncio.gather(*tasks)
        if self.status:
            print(f"{self.upName} 已完成!")
            self.draw()
        else:
            print("查询失败，请等待十分钟再次尝试")

    def run(self):
        start = time.time()
        asyncio.run(self.main())
        print(f"用时{time.time()-start:.2f}秒")


if __name__ == "__main__":
    while 1:
        uid = input("请输入需要爬取的用户uid: ")
        if uid.isnumeric():
            break
        else:
            print("格式有误，请重新输入纯数字!")
    Spyder(uid).run()
    fine = input("\n按回车键退出...")
