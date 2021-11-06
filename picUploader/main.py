import os, requests
from config import cookies


def image_upload(file_path):
    api_url = "https://api.vc.bilibili.com/api/v1/drawImage/upload"
    with open(file_path, "rb") as f:
        img_file = f.read()
    files = {"file_up": (file_name, img_file)}
    data = {
        "biz": "draw",
        "category": "daily",
    }
    headers = {
        "Origin": "https://t.bilibili.com",
        "Referer": "https://t.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    }
    r = requests.post(
        api_url,
        files=files,
        data=data,
        headers=headers,
        cookies=cookies,
        timeout=300,
    ).json
    img_url = r["data"]["image_url"]
    print(f"Url: {img_url}")
    return img_url


if __name__ == "__main__":
    if len(os.sys.argv) == 2:
        file_name = os.sys.argv[1]
        file_path = os.path.abspath(file_name)
        print("图片上传中...")
    else:
        print("格式有误！上传示例图片example.png...")
        file_path = os.path.join(os.sys.path[0], "example.png")
    image_upload(file_path)
