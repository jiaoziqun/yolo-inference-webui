from contextlib import asynccontextmanager
from fastapi import FastAPI,UploadFile,File
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
import os

import torch

models = {}
app_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(app_path)

@asynccontextmanager
async def lifespan(app_instance: FastAPI):#其中app_instance是接收参数，FastAPI内部调用的时候会传递进来的
    #startup,yield之前
    models["yolo"] = torch.hub.load(
        f"{root_path}/yolov5-master",
        "custom",
        f"{root_path}/yolov5-master/weights/yolov5s.pt",
        source="local",
    )

    yield

    #shutdown，yield之后

app = FastAPI(lifespan = lifespan)

@app.get("/")
def index():
    return FileResponse(os.path.join(root_path, "static", "index.html"))


@app.get("/health") # 有get、post、put、delete
def health():
    if models.get("yolo") is not None:
        return {"status": "ok", "model_loaded": True, "model_name": "yolov5s"}
    else:
        return {"status": "bad", "model_loaded": False, "model_name": "error"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):#使用协程读取文件
    content = await file.read()
    img = Image.open(BytesIO(content))
    results = models["yolo"](img)
    
    if results:
        result = results.pandas()
        count = 0
        return_result = []

        for i in range(len(result.xyxy)):  # 第几张图
            detections = []
            count = result.xyxy[i].shape[0]

            for _, row in result.xyxy[i].iterrows():  # 第几个目标, 注意iterrows这个方法返回行索引+行数据

                cls = models["yolo"].names[row.name]
                confidence = row.confidence
                xmin = row.xmin
                xmax = row.xmax
                ymin = row.ymin
                ymax = row.ymax

                w_det = max(0, xmax - xmin)
                h_det = max(0, ymax - ymin)
                bbox = [xmin, ymin, w_det, h_det]

                detections.append(
                    {"class": cls, "confidence": confidence, "bbox": bbox}
                )  # 框信息

            if count <= 0:
                raise ValueError("目标数目为0但进入到检测到目标区域")

            return_result.append(
                {"success": True, "detections": detections, "count": count}
            )
        return return_result

    else:
        return {
            "success": False,
            "detections": [],
            "count": 0,
        }  # 结构化JSON，没检测到也得返回这个格式
