## EmoGo Backend 資料匯出 (Data Export) URI

**主要資料匯出端點 URI:** [https://emogo-backend-ruby04hung.onrender.com/export](https://emogo-backend-ruby04hung.onrender.com/export)

---

## 學生資訊
- **姓名:** 洪于茹
- **學號:** R14546007  
- **課程:** 心理資訊學與神經資訊學
- **作業:** Week 13 - FastAPI + MongoDB

## 部署狀態
✅ **服務運行中:** https://emogo-backend-ruby04hung.onrender.com/

## API 端點
| 端點 | 方法 | 說明 |
|------|------|------|
| `/` | GET | 首頁 (HTML 頁面) |
| `/export` | GET | 匯出所有數據 |
| `/health` | GET | 健康檢查 |
| `/docs` | GET | Swagger API 文檔 |
| `/vlogs` | GET | 取得影片數據 |
| `/emotions` | GET | 取得情緒數據 |
| `/gps` | GET | 取得位置數據 |
| `/download` | GET | 下載數據檔案 - 自動下載 JSON 檔案 |
| `/download/videos` | GET | 下載所有影片為 ZIP 壓縮檔 |
| `/videos` | GET | 列出所有可下載的影片 |
| `/videos/{video_id}` | GET | 下載單一影片檔案 |

## 數據類型
1. **Vlogs (影片紀錄)** - 1秒鐘情緒影片
2. **Emotions (情緒數據)** - 1-5分情緒評分
3. **GPS (位置數據)** - 經緯度位置資訊

## 技術架構
- **後端框架:** FastAPI (Python 3.8+)
- **資料庫:** MongoDB Atlas
- **部署平台:** Render
- **API 格式:** RESTful JSON
- **檔案格式:** JSON、MP4、ZIP

---
### 1. GitHub Repository
https://github.com/ntu-info/emogo-backend-ruby04hung

### 2. 部署網址（首頁）
https://emogo-backend-ruby04hung.onrender.com/

### 3. 主要需求端點（資料匯出）
https://emogo-backend-ruby04hung.onrender.com/export

### 4. 資料下載端點
https://emogo-backend-ruby04hung.onrender.com/download

### 5. 影片壓縮檔下載
https://emogo-backend-ruby04hung.onrender.com/download/videos

### 6. 健康檢查端點（確認 MongoDB 連線）
https://emogo-backend-ruby04hung.onrender.com/health

### 7. API 文檔
https://emogo-backend-ruby04hung.onrender.com/docs

---

## 功能說明
1. ✅ 使用 FastAPI 框架
2. ✅ 連接 MongoDB Atlas 資料庫
3. ✅ 提供三種類型數據：Vlogs、Emotions、GPS
4. ✅ 符合作業所有要求
5. ✅ 部署於 Render 公開伺服器

---

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e7FBMwSa)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21912409&assignment_repo_type=AssignmentRepo)

# Deploy FastAPI on Render

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.

See https://render.com/docs/deploy-fastapi or follow the steps below:

## Manual Steps
1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

6. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks
Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!
