import time, httpx, asyncio, aiohttp


class Down:
    def __init__(self):
        self.fi = 0
        self.total = 400
        url = "https://ayatale.coding.net/p/picbed/d/kemo/git/raw/master/"
        self.urls = [f"{url}{_}.jpg" for _ in range(self.total)]

    def bar(self):
        val = 50 * self.fi / self.total
        text = f" {val/50:.2%}[{'='*int(val)}>{' '*(50-int(val))}] {self.fi} of {self.total}\r"
        print(text, end="", flush=True)

    async def aioDown(self, url):
        r = await self.client.get(url)
        raw = await r.read()
        with open(f"aiojpg/{self.fi}.jpg", "wb+") as f:
            f.write(raw)
        self.fi += 1
        self.bar()

    async def aioMain(self):
        async with aiohttp.ClientSession() as self.client:
            tasks1 = [self.aioDown(u) for u in self.urls]
            await asyncio.gather(*tasks1)

    async def httpxDown(self, url):
        r = await self.client2.get(url)
        with open(f"httpxjpg/{self.fi}.jpg", "wb+") as f:
            f.write(r.content)
        self.fi += 1
        self.bar()

    async def httpxMain(self):
        async with httpx.AsyncClient() as self.client2:
            tasks2 = [self.httpxDown(u) for u in self.urls]
            await asyncio.gather(*tasks2)

    def run(self):
        start = time.time()
        asyncio.run(self.httpxMain())
        print(f"\nHttpx Cost time: {time.time()-start:.2f}s")
        self.fi = 0
        time.sleep(1)
        start2 = time.time()
        asyncio.run(self.aioMain())
        print(f"\nAiohttp Cost time: {time.time()-start2:.2f}s")


if __name__ == "__main__":
    Down().run()
