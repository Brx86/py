import os, requests
from config import cookies

# 定义上传函数
def image_upload(file_path):
    # api地址
    api_url = "https://api.vc.bilibili.com/api/v1/drawImage/upload"

    # 打开图片文件
    with open(file_path, "rb") as f:
        img_file = f.read()

    # 设置post参数
    files = {"file_up": (file_path, img_file)}
    data = {
        "biz": "draw",
        "category": "daily",
    }
    headers = {
        "Origin": "https://t.bilibili.com",
        "Referer": "https://t.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    }

    # 向api发送post请求
    r = requests.post(
        api_url,
        files=files,
        data=data,
        headers=headers,
        cookies=cookies,
        timeout=300,
    )

    # 解析返回值，得到图片链接并请求api得到短链接
    img_url = r.json()["data"]["image_url"]

    r = requests.get(f"https://bili.fan/api/bili.php?b23tvurl={img_url}")
    short_url = r.json()["data"]["content"]

    # 输出结果
    print(f"图片链接: {img_url}\n短网址:   {short_url}")
    return img_url, short_url


if __name__ == "__main__":
    if len(os.sys.argv) == 2:
        file_name = os.sys.argv[1]
        file_path = os.path.abspath(file_name)
        print("图片上传中...")
    else:
        print("格式有误！上传示例图片example.png...")
        file_path = os.path.join(os.sys.path[0], "example.png")
    image_upload(file_path)
