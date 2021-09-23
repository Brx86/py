import os, re, time, requests, asyncio, aiohttp


class Spyder:
    def vaTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        self.title = re.sub(rstr, "_", title)  # 替换为下划线

    def getName(self):
        userApi = f"https://api.bilibili.com/x/web-interface/card?mid={self.uid}"
        up = self.session.get(userApi).json()["data"]["card"]["name"]
        print(f"正在处理用户“{up}”...")

    def getList(self):
        pn, cvList = 1, []
        api = f"https://api.bilibili.com/x/space/article?mid={self.uid}&pn={pn}"
        data = self.session.get(api).json()["data"]
        pages = int(data["count"]) // 30 + 1
        print(f"Getting page {pn}/{pages}...")
        cvList.extend(data["articles"])
        while pn < pages:
            pn += 1
            print(f"Getting page {pn}/{pages}...")
            api = f"https://api.bilibili.com/x/space/article?mid={self.uid}&pn={pn}"
            data = self.session.get(api).json()["data"]
            cvList.extend(data["articles"])
        self.total = len(cvList)
        print(f"共有{self.total}篇专栏!")
        return cvList

    def getUrl(self, cvid, pTime):
        html = self.session.get(f"https://www.bilibili.com/read/cv{cvid}")
        partten = re.compile(r"article\/([0-9A-z]{40}).(jpg|png|gif)")
        imgList = partten.findall(html.text)
        print(f"正在处理cv{cvid}: [{self.title}]")
        if imgList:
            self.write(imgList, pTime)

    def write(self, imgList, pTime):
        x = 0
        tTime = time.strftime("%Y%m%d%H%M%S", time.localtime(pTime))
        if self.yn == "1":
            fName = f"uid{self.uid}.txt"
        else:
            fName = f"cv{self.uid}.txt"
        for img in imgList:
            x += 1
            self.num += 1
            pic = f"{img[0]}.{img[1]}"
            with open(fName, "a+") as f:
                f.write(
                    f"{self.title},{tTime}-{x},http://i0.hdslb.com/bfs/article/{pic}\n"
                )

    def main(self, uid, yn):
        self.num, self.uid, self.yn = 0, uid, yn
        self.session = requests.session()
        self.getName()
        if yn == "1":
            cvList = self.getList()
            if os.path.exists(f"{self.uid}.txt"):
                os.remove(f"{self.uid}.txt")
            for cv in cvList:
                self.vaTitle(cv["title"])
                self.getUrl(cv["id"], cv["publish_time"])
            print(f"总共有{self.num}张图片！")
        else:
            pass


class Down:
    def bar(self):
        val = 50 * self.fi / self.total
        text = f" {val/50:.2%}[{'='*int(val)}>{' '*(50-int(val))}] {self.fi} of {self.total}\r"
        print(text, end="", flush=True)

    async def downPic(self, line):
        line = line.split(",")
        url = line[2].strip()
        fileType = url.split(".")[-1]
        fileName = f"{line[1]}.{fileType}"
        r = await self.session.get(url)
        raw = await r.read()
        with open(f"{self.name}/{fileName}", "wb+") as f:
            f.write(raw)
        self.fi += 1
        self.bar()

    async def main(self):
        self.fi = 0
        async with aiohttp.ClientSession() as self.session:
            if not os.path.exists(self.name):
                os.mkdir(self.name)
            with open(f"{self.name}.txt", "r") as f:
                uList = f.readlines()
            self.total = len(uList)
            tasks = [self.downPic(l) for l in uList]
            await asyncio.gather(*tasks)

    def run(self, uid, yn):
        if yn == "1":
            self.name = f"uid{uid}"
        else:
            self.name = f"cv{uid}"
        s = time.time()
        asyncio.run(self.main())
        e = time.time()
        print(f"\n执行结束，耗时{e-s:.2f}s")


if __name__ == "__main__":
    while 1:
        yn = input("请选择爬取内容(输入1/2)：\n    1.指定用户的全部专栏图片\n    2.指定单个专栏的全部图片\n")
        if yn == "1" or yn == "2":
            break
        else:
            print("格式有误，请输入1或2!")
    while 1:
        if yn == "1":
            uid = input("请输入需要爬取的用户uid: ")
        else:
            uid = input("请输入需要爬取的专栏cv号: ")
        if uid.isnumeric():
            break
        else:
            print("格式有误，请重新输入纯数字!")
    while 1:
        judge = input("爬取链接后是否下载? (y/n) ")
        Spyder().main(uid, yn)
        if judge == "y" or judge == "":
            Down().run(uid, yn)
            break
        elif judge == "n":
            break
        else:
            print("格式有误，请重新输入y或n!")
