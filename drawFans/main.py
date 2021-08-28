import os, csv, time, random, requests, threadpool


def getName(mid):
    global session
    userApi = f"https://api.bilibili.com/x/web-interface/card?mid={mid}"
    up = session.get(userApi).json()["data"]
    upName = up["card"]["name"]
    upFans = int(up["follower"])
    if upFans < 250:
        upPages = int(upFans) // 50 + 1
    else:
        upPages = 5
    return upName, upPages


def getFans(mid, i):
    global session
    print(f"Searching page {i+1}...")
    fansApi = f"http://api.bilibili.com/x/relation/followers?vmid={mid}&pn={i+1}"
    return session.get(fansApi).json()["data"]["list"]


def getInfo(u):
    global session
    userApi = f"http://api.bilibili.com/x/space/acc/info?mid={u['mid']}&jsonp"
    try:
        ui = session.get(userApi).json()["data"]
        print(f"UID: {u['mid']}\tLevel: {ui['level']}")
        with open(f"{up[0]}/fans.csv", "a+") as f:
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
    except TypeError:
        print("请求被拦截，请勿频繁使用!")


if __name__ == "__main__":
    t0 = time.time()
    session = requests.Session()
    upMid = os.sys.argv[1]
    up = getName(upMid)
    uList, fList = [], []
    if not os.path.exists(up[0]):
        os.mkdir(up[0])
    with open(f"{up[0]}/fans.csv", "w+") as f:
        f.write("uid,mtime,uname,vipType,level,sex,sign\n")
    for i in range(up[1]):
        uList.extend(getFans(upMid, i))
    pool = threadpool.ThreadPool(20)
    tasks = threadpool.makeRequests(getInfo, uList)
    [pool.putRequest(task) for task in tasks]
    pool.wait()
    print(f"Cost {time.time()-t0} secs")
    print(f"{up[0]} Finished！")
