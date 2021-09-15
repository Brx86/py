import os, re, down, time, requests


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
        yield str(page)
        time.sleep(0.4)
        offset = page["next_offset"]
        if page["has_more"]:
            print(f"已爬取第{p}页，下一页offset为{offset}")
        else:
            print(f"共{p-1}页，爬取完成！")
            break


def getCard(uid):
    num = 0
    pageGen = getPage(uid)
    partten = re.compile(r"album\\\\/([0-9A-z]{40}).(jpg|png|gif)")
    for page in pageGen:
        imgList = partten.findall(page)
        if imgList:
            for img in imgList:
                num += 1
                pic = f"{img[0]}.{img[1]}"
                with open(f"{uid}.txt", "a+") as f:
                    f.write(f"http://i0.hdslb.com/bfs/album/{pic}\n")
    print(f"总共有{num}张图片！")


def main(uid):
    global session
    session = requests.Session()
    if os.path.exists(f"{uid}.txt"):
        os.remove(f"{uid}.txt")
    getCard(uid)


if __name__ == "__main__":
    if len(os.sys.argv) == 2:
        main(os.sys.argv[1])
    else:
        while 1:
            uid = input("请输入需要爬取的用户UID: ")
            if uid.isnumeric():
                break
            else:
                print("格式有误，请重新输入！")
        while 1:
            yn = input("爬取链接后是否下载? (y/n) ")
            if yn == "y" or yn == "":
                main(uid)
                down.main(uid)
                break
            elif yn == "n":
                main(uid)
                break
            else:
                print("格式有误，请重新输入！")
