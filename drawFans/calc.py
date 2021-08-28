import os, csv, time, requests
from pyecharts import options as opts
from py.charts import Page, Pie


def getName(mid):
    userApi = f"https://api.bilibili.com/x/web-interface/card?mid={mid}"
    up = requests.get(userApi).json()["data"]
    return = up["card"]["name"]


upMid = os.sys.argv[1]
upDir = getName(upMid)

lvList = [[f"lv{x}", 0] for x in range(7)]
with open(f"{upDir}/fans.csv", "r") as f1:
    rCsv = csv.reader(f1)
    for line in rCsv:
        lv = line[4]
        if not line[4].isdigit():
            continue
        lv = int(lv)
        lvList[lv][1] += 1


sumUsers = 0
for u in range(7):
    sumUsers += lvList[u][1]
for u in range(7):
    lvList[u][1] = round(100 * lvList[u][1] / sumUsers, 2)


tTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 30))
pie = (
    Pie()
    .add("", lvList, radius=["30%", "70%"], center=["55%", "50%"])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{upDir} 粉丝等级占比",
            subtitle=f"最后更新于: {tTime}\n\nUID: {upMid}   样本数: {sumUsers}",
            pos_left="15%",
        ),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="30%", pos_left="15%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
)

pie.render(f"{upDir}/pie.html")
print("Chart Generated!")
