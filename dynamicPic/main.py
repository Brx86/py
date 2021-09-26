import os, re, time, requests, threadpool


def bar():
    val = 50 * n / total
    text = f" {val/50:.2%}[{'='*int(val)}>{' '*(50-int(val))}] {n} of {total}\r"
    print(text, end="", flush=True)


def downPic(line, uid):
    global n
    line = line.split(",")
    url = line[1].strip()
    fileType = url.split(".")[-1]
    fileName = f"{line[0]}.{fileType}"
    raw = session.get(url)
    with open(f"{uid}/{fileName}", "wb+") as f:
        f.write(raw.content)
    n += 1
    bar()


def down(uid):
    t0 = time.time()
    global n, total, session
    session = requests.Session()
    n = 0
    if not os.path.exists(uid):
        os.mkdir(uid)
    with open(f"{uid}.txt", "r") as f:
        uList = f.readlines()
    total = len(uList)
    pool = threadpool.ThreadPool(8)
    tList = [([line, uid], 0) for line in uList]
    tasks = threadpool.makeRequests(downPic, tList)
    [pool.putRequest(task) for task in tasks]
    pool.wait()
    cost = time.time() - t0
    print(f"\n全部图片下载完成, 用时{cost:.2f}秒!")


def getName(uid):
    userApi = f"https://api.bilibili.com/x/web-interface/card?mid={uid}"
    try:
        up = session.get(userApi).json()["data"]["card"]["name"]
    except TypeError:
        print("该用户不存在!")
    print(f"正在抓取用户“{up}”的动态图片...")


def getPage(uid):
    p, offset = 0, ""
    while 1:
        p += 1
        params = {"host_uid": uid, "need_top": 1, "offset_dynamic_id": offset}
        page = session.get(
            "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history",
            params=params,
            timeout=5,
        ).json()["data"]
        # time.sleep(0.4)
        offset = page["next_offset"]
        if page["has_more"]:
            print(f"正在处理第{p}页, 下一页offset为{offset}")
            yield page["cards"]
        else:
            print(f"共{p-1}页, 爬取完成!")
            break


def getCard(uid):
    num = 0
    pageGen = getPage(uid)
    partten = re.compile(r"album\\/([0-9A-z]{40}).(jpg|png|gif)")
    for page in pageGen:
        for card in page:
            imgList = partten.findall(str(card["card"]))
            if imgList:
                x = 0
                tTime = time.strftime(
                    "%Y%m%d%H%M%S", time.localtime(card["desc"]["timestamp"])
                )
                for img in imgList:
                    x += 1
                    num += 1
                    pic = f"{img[0]}.{img[1]}"
                    with open(f"{uid}.txt", "a+") as f:
                        f.write(f"{tTime}-{x},http://i0.hdslb.com/bfs/album/{pic}\n")
    if num:
        print(f"总共有{num}张图片!")
    else:
        print("该用户动态没有图片!")
        fine = input("\n按回车键退出...")
        exit()


def main(uid):
    global session
    session = requests.Session()
    if os.path.exists(f"{uid}.txt"):
        os.remove(f"{uid}.txt")
    getName(uid)
    getCard(uid)


if __name__ == "__main__":
    while 1:
        uid = input("请输入需要爬取的用户UID: ")
        if uid.isnumeric():
            break
        else:
            print("格式有误, 请重新输入!")
    while 1:
        yn = input("爬取链接后是否下载? (y/n) ")
        if yn == "y" or yn == "":
            main(uid)
            down(uid)
            break
        elif yn == "n":
            main(uid)
            break
        else:
            print("格式有误, 请重新输入!")
    fine = input("\n按回车键退出...")
