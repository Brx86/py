import os, time, requests, threadpool


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


def main(uid):
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
    print(f"\n全部图片下载完成，用时{cost:.2f}秒！")


if __name__ == "__main__":
    uid = os.sys.argv[1]
    main(uid)
