#并发压测
import asyncio
import time
import httpx
import mimetypes
import os

async def send_one(client, url, image_path):
    """发一个请求，返回耗时（秒）"""
    t1 = time.time()
    mime = mimetypes.guess_type(image_path)[0]
    file_name = os.path.basename(image_path)
    with open(image_path,"rb") as img_rb:
        file = {"file": (file_name, img_rb, mime)}
        result = await client.post(url, files = file)
        print(f"{result.json()[0]['detections']}")
    t2 = time.time()
    return t2 - t1

async def main():
    url = "http://localhost:8000/detect"
    image_path = r"C:\Users\h2\Desktop\work\P4\yolov5-master\data\images\bus.jpg"
    n_requests = 10
    sum_t = 0.0
    QPS_t = 0.0
    async with httpx.AsyncClient() as client:
        tasks = [send_one(client, url, image_path) for _ in range(n_requests)]
        t = await asyncio.gather(*tasks)  
        max_t = max(t)
        sum_t = sum(t)
    QPS_t = n_requests/max_t
    print(f"总耗时为{sum_t}")
    print(f"最大耗时为{max_t}")
    print(f"QPS为{QPS_t}")

if __name__ == "__main__":
    asyncio.run(main())