import os, time, requests, threadpool


def bar():
    val = 50 * n / total
    text = f" {val/50:.2%}[{'='*int(val)}>{' '*(50-int(val))}] {n} of {total}\r"
    print(text, end="", flush=True)


def downPic(line):
    global n
    url = line.strip()
    name = url.split("/")[-1]
    raw = session.get(url)
    with open(f"{uid}/{name}", "wb+") as f:
        f.write(raw.content)
    n += 1
    bar()


def main():
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
    tasks = threadpool.makeRequests(downPic, uList)
    [pool.putRequest(task) for task in tasks]
    pool.wait()
    cost = time.time() - t0
    print(f"\n全部图片下载完成，用时{cost:.2f}秒！")


if __name__ == "__main__":
    uid = os.sys.argv[1]
    main()
