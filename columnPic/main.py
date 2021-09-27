import os, re, time, requests, threadpool


class Spyder:
    def vaTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        self.title = re.sub(rstr, "_", title)

    def getName(self):
        userApi = f"https://api.bilibili.com/x/web-interface/card?mid={self.uid}"
        up = self.session.get(userApi).json()["data"]["card"]["name"]
        print(f"正在处理用户“{up}”...")

    def getList(self):
        pn, cvList = 1, []
        api = f"https://api.bilibili.com/x/space/article?mid={self.uid}&pn={pn}"
        data = self.session.get(api).json()["data"]
        try:
            pages = (int(data["count"]) - 1) // 30 + 1
        except KeyError:
            print("该用户没有专栏!")
            fine = input("\n按回车键退出...")
            exit()
        print(f"正在获取专栏列表 {pn}/{pages}...")
        cvList.extend(data["articles"])
        while pn < pages:
            pn += 1
            print(f"正在获取专栏列表 {pn}/{pages}...")
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
        if pTime:
            print(f"正在处理cv{cvid}: [{self.title}]")
        else:
            print(f"正在处理cv{cvid}...")
        if imgList:
            self.write(imgList, pTime)

    def write(self, imgList, pTime):
        x, form = 0, "%Y%m%d%H%M%S"
        tTime = time.strftime(form, time.localtime(pTime)) if pTime else self.uid
        fName = f"uid{self.uid}.txt" if self.yn == "1" else f"cv{self.uid}.txt"
        for img in imgList:
            x += 1
            self.num += 1
            with open(fName, "a+") as f:
                url = f"http://i0.hdslb.com/bfs/article/{img[0]}.{img[1]}\n"
                f.write(f"{self.title},{tTime}-{x},{url}")

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
            self.title = 0
            self.getUrl(uid, 0)


class Down:
    def bar(self):
        val = 50 * self.fi / self.total
        text = f" {val/50:.2%}[{'='*int(val)}>{' '*(50-int(val))}] {self.fi} of {self.total}\r"
        print(text, end="", flush=True)

    def downPic(self, line):
        line = line.split(",")
        url = line[2].strip()
        fileType = url.split(".")[-1]
        fileName = f"{line[1]}.{fileType}"
        with self.session.get(url) as raw:
            with open(f"{self.name}/{fileName}", "wb+") as f:
                f.write(raw.content)
        self.fi += 1
        self.bar()

    def main(self):
        self.fi = 0
        self.session = requests.session()
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        with open(f"{self.name}.txt", "r") as f:
            uList = f.readlines()
        self.total = len(uList)
        pool = threadpool.ThreadPool(8)
        tasks = threadpool.makeRequests(self.downPic, uList)
        [pool.putRequest(task) for task in tasks]
        pool.wait()

    def run(self, uid, yn):
        self.name = f"uid{uid}" if yn == "1" else f"cv{uid}"
        start = time.time()
        self.main()
        print(f"\n全部图片下载完成，用时 {time.time()-start:.2f}s")


if __name__ == "__main__":
    while 1:
        yn = input("请选择爬取内容: \n    1.指定用户的全部专栏图片\n    2.指定单个专栏的全部图片\n(输入1/2) ")
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
    fine = input("\n按回车键退出...")
