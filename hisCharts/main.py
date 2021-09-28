import os, csv, time, requests
from pyecharts import options as opts
from pyecharts.charts import Pie, Page, WordCloud
import platform

headers = {
    "cookie": "buvid3=9923EC96-6FCC-5EC8-B06F-837C8DD0599C26087infoc; CURRENT_FNVAL=80; _uuid=F214B2B2-BD8C-C108-C5C9-49C3FD767B7B26428infoc; blackside_state=1; rpdid=|(k|kmku~u|u0J'uYk)R)l|km; sid=9zz28kep; fingerprint=cf5e667025e31a8994a65020aa241f37; buvid_fp=9923EC96-6FCC-5EC8-B06F-837C8DD0599C26087infoc; buvid_fp_plain=9923EC96-6FCC-5EC8-B06F-837C8DD0599C26087infoc; SESSDATA=98a40580%2C1646962507%2C5526d%2A91; bili_jct=4c385f2aba2dd256cd93f8dce6b05ba2; DedeUserID=25773550; DedeUserID__ckMd5=443fa8253a08a5d6; PVID=1; bp_t_offset_25773550=575134066971618448; balh_server_inner=__custom__; balh_is_closed=; LIVE_BUVID=AUTO7316327467091875; fingerprint3=40102fa238adc44617b15b33fa39bac7; fingerprint_s=4f6f115e7d3e7807c05f3063572adab0; innersign=0; bsource=search_baidu; bfe_id=0c3a1998eda2972db3dbce4811a80de6"
}


class Spyder:
    def __init__(self):
        self.session = requests.Session()

    def getVideo(self, v):
        if v["tag_name"]:
            viewTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(v["view_at"]))
            return [
                v["history"]["oid"],
                v["title"].replace(",", "，").replace('"', "“"),
                v["author_name"],
                v["author_mid"],
                v["tag_name"],
                viewTime,
            ]

    def getPage(self):
        p, max_, at_ = 0, "", ""
        while 1:
            p += 1
            page = self.session.get(
                f"https://api.bilibili.com/x/web-interface/history/cursor?max={max_}&view_at={at_}",
                headers=headers,
            ).json()["data"]
            time.sleep(0.4)
            yield page
            max_ = page["cursor"]["max"]
            at_ = page["cursor"]["view_at"]
            if max_:
                print(f"已爬取第{p}页，下一页为{at_}-{max_}")
            else:
                print(f"已爬取第{p}页，爬取完成！")
                break

    def run(self):
        hisGen = self.getPage()
        with open("history.csv", "w+") as f:
            f.write("avid,title,author,authorID,tagName,viewTime\n")
        with open("history.csv", "a+") as f:
            wCsv = csv.writer(f)
            for his in hisGen:
                for v in his["list"]:
                    vInfo = self.getVideo(v)
                    if vInfo:
                        wCsv.writerow(vInfo)


class Draw:
    def __init__(self):
        self.total = 0
        self.centList = []
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def readData(self):
        tagDict = {}
        with open("history.csv", "r") as f:
            rCsv = csv.reader(f)
            for line in rCsv:
                self.total += 1
                vType = line[4]
                if vType in tagDict:
                    tagDict[vType] += 1
                else:
                    tagDict[vType] = 1
        self.sortList = sorted(
            tagDict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True
        )

        other = 0
        for i in range(29):
            percent = round(100 * self.sortList[i][1] / self.total, 2)
            self.centList.append([self.sortList[i][0], percent])
        for i in range(29, len(self.sortList)):
            other += self.sortList[i][1]
        self.centList.append(["其他", round(100 * other / self.total, 2)])
        return self.centList, self.sortList

    def drawPie(self):
        pie = (
            Pie()
            .add("", self.centList, radius=["25%", "50%"], center=["50%", "60%"])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="最近播放各分区百分比",
                    subtitle=f"样本量: {self.total}   最后更新于: {self.time}",
                    pos_left="center",
                    pos_top="8",
                ),
                legend_opts=opts.LegendOpts(orient="", pos_top="13%"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
        )
        pie.render("pie.html")

    def drawCloud(self):
        cloud = WordCloud().add(
            "",
            self.sortList,
            shape="diamond",
            # word_size_range=[20, 80],
        )
        cloud.render("cloud.html")

    def run(self):
        start = time.time()
        self.readData()
        self.drawPie()
        self.drawCloud()
        if platform.system() == "Windows":
            os.system("copy pie.html+cloud.html index.html")
        elif platform.system() == "Linux":
            os.system("cat pie.html cloud.html >index.html")
        print(f"Charts Generated! Cost {time.time()-start:.2f}s")


if __name__ == "__main__":
    Spyder().run()
    Draw().run()
