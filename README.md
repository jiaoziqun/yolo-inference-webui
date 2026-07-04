![last_commit](https://img.shields.io/github/last-commit/jiaoziqun/action_test)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

本项目利用FastAPI、Vue以及YOLOv5搭建了一个本地前端网页模型推理平台
模型采用官方发布的COCO数据集训练的YOLOV5S，旨在学习YOLO+后端FastAPI服务器+Vue前端+并发压测计算QPS的流程
安装完docker后先运行docker compose build再运行docker compose up -d启动服务器，之后访问本地localhost:8000即可
## 技术栈

| 层级 | 技术 |
|------|------|
| 模型推理 | YOLOv5s（COCO pretrained） |
| 后端 API | FastAPI + Uvicorn |
| 前端 | Vue 3（CDN）+ Canvas |
| 容器化 | Docker + Docker Compose |
| 压测 | httpx + asyncio |

项目最终前端运行结果如下图:
![项目前端运行结果](./网页结果.png)