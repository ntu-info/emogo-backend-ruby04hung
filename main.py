from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response, FileResponse
from pymongo import MongoClient
from datetime import datetime
import os
import json
import urllib.parse
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel

# 載入環境變數
load_dotenv()

# 建立 FastAPI 應用程式
app = FastAPI(
    title="EmoGo Backend API",
    description="Week 13 - FastAPI + MongoDB 作業",
    version="1.0.0"
)

# MongoDB 連線設定
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URL)
db = client["emogo_db"]

# 影片相關設定
BASE_URL = os.getenv("BASE_URL", "https://emogo-backend-ruby04hung.onrender.com")
VIDEO_DIR = "sample_videos"

# 建立集合
vlogs_collection = db["vlogs"]
emotions_collection = db["emotions"]
gps_collection = db["gps"]

# 資料模型
class VlogData(BaseModel):
    id: str
    description: str
    timestamp: str
    student: str = "洪于茹"
    student_id: str = "R14546007"

class EmotionData(BaseModel):
    id: str
    sentiment: int
    scale: str = "1-5 (1=very bad, 5=very good)"
    timestamp: str
    student: str = "洪于茹"
    student_id: str = "R14546007"

class GPSData(BaseModel):
    id: str
    latitude: float
    longitude: float
    timestamp: str
    student: str = "洪于茹"
    student_id: str = "R14546007"

# HTML 首頁
@app.get("/", response_class=HTMLResponse)
def root():
    try:
        # 檢查 MongoDB 連線
        client.server_info()
        db_status = "✅ 已連線"
        db_color = "#4CAF50"
    except:
        db_status = "❌ 未連線"
        db_color = "#f44336"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EmoGo Backend API - 洪于茹 (R14546007)</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Microsoft JhengHei', 'Segoe UI', sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 40px auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 50px 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.8rem;
                margin-bottom: 15px;
            }}
            
            .header p {{
                font-size: 1.2rem;
                opacity: 0.95;
            }}
            
            .student-info {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                display: inline-block;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .status-card {{
                display: flex;
                align-items: center;
                margin-bottom: 30px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 15px;
                border-left: 5px solid #667eea;
            }}
            
            .status-icon {{
                font-size: 3rem;
                margin-right: 25px;
            }}
            
            .status-details h2 {{
                color: #667eea;
                margin-bottom: 10px;
            }}
            
            .database-status {{
                display: inline-block;
                padding: 8px 20px;
                background: {db_color};
                color: white;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 10px;
            }}
            
            .endpoints-section {{
                margin-top: 40px;
            }}
            
            .section-title {{
                color: #764ba2;
                font-size: 1.8rem;
                margin-bottom: 25px;
                padding-bottom: 10px;
                border-bottom: 2px solid #eee;
            }}
            
            .endpoint-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            
            .endpoint-card {{
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 25px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }}
            
            .endpoint-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                border-color: #667eea;
            }}
            
            .endpoint-card h3 {{
                color: #333;
                margin-bottom: 15px;
                font-size: 1.3rem;
            }}
            
            .endpoint-path {{
                font-family: 'Consolas', monospace;
                background: #f5f5f5;
                padding: 10px 15px;
                border-radius: 8px;
                margin: 15px 0;
                color: #d63384;
                font-weight: bold;
                word-break: break-all;
            }}
            
            .endpoint-desc {{
                color: #666;
                margin-bottom: 20px;
                line-height: 1.5;
            }}
            
            .btn {{
                display: inline-block;
                padding: 12px 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            
            .btn-secondary {{
                background: #6c757d;
            }}
            
            .btn-secondary:hover {{
                background: #5a6268;
            }}
            
            .data-types {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .data-card {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
            }}
            
            .data-card h3 {{
                font-size: 1.5rem;
                margin-bottom: 10px;
            }}
            
            .data-icon {{
                font-size: 2.5rem;
                margin-bottom: 15px;
            }}
            
            .footer {{
                text-align: center;
                padding: 30px;
                color: #666;
                background: #f8f9fa;
                border-top: 1px solid #eee;
            }}
            
            .course-info {{
                font-size: 0.9rem;
                margin-top: 10px;
                color: #888;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    margin: 20px auto;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .header h1 {{
                    font-size: 2.2rem;
                }}
                
                .content {{
                    padding: 20px;
                }}
                
                .status-card {{
                    flex-direction: column;
                    text-align: center;
                }}
                
                .status-icon {{
                    margin-right: 0;
                    margin-bottom: 20px;
                }}
                
                .endpoint-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- 頁首 -->
            <div class="header">
                <h1>🎭 EmoGo 情緒追蹤系統</h1>
                <p>FastAPI + MongoDB 後端服務</p>
                <div class="student-info">
                    <strong>學生：</strong>洪于茹 (R14546007)<br>
                    <strong>課程：</strong>心理資訊學與神經資訊學
                </div>
            </div>
            
            <!-- 主要內容 -->
            <div class="content">
                <!-- 狀態卡片 -->
                <div class="status-card">
                    <div class="status-icon">🚀</div>
                    <div class="status-details">
                        <h2>服務狀態</h2>
                        <p><strong>部署位置：</strong>Render.com</p>
                        <p><strong>服務狀態：</strong>運行中</p>
                        <p><strong>資料庫狀態：</strong> <span class="database-status">{db_status}</span></p>
                        <p><strong>作業編號：</strong>Week 13 - FastAPI + MongoDB</p>
                    </div>
                </div>
                
                <!-- 數據類型 -->
                <h2 class="section-title">📊 支援的數據類型</h2>
                <div class="data-types">
                    <div class="data-card">
                        <div class="data-icon">🎥</div>
                        <h3>影片紀錄 (Vlogs)</h3>
                        <p>1秒鐘情緒影片</p>
                    </div>
                    <div class="data-card">
                        <div class="data-icon">😊</div>
                        <h3>情緒數據 (Emotions)</h3>
                        <p>1-5分情緒評分</p>
                    </div>
                    <div class="data-card">
                        <div class="data-icon">📍</div>
                        <h3>位置數據 (GPS)</h3>
                        <p>經緯度位置資訊</p>
                    </div>
                </div>
                
                <!-- API 端點 -->
                <h2 class="section-title">🚀 API 端點</h2>
                <div class="endpoint-grid">
                    <!-- 主要需求端點 -->
                    <div class="endpoint-card">
                        <h3>📤 匯出數據 (主要需求)</h3>
                        <div class="endpoint-path">GET /export</div>
                        <div class="endpoint-desc">
                            匯出所有數據（vlogs, emotions, GPS）為 JSON 格式。<br>
                            <strong>這是作業的主要要求！</strong>
                        </div>
                        <a href="/export" class="btn" target="_blank">測試此端點</a>
                    </div>

                    <!-- 下載數據端點 -->
                    <div class="endpoint-card">
                        <h3>💾 下載數據檔案</h3>
                        <div class="endpoint-path">GET /download</div>
                        <div class="endpoint-desc">
                            下載所有數據（vlogs, emotions, GPS）為 JSON 檔案。
                        </div>
                        <a href="/download" class="btn" style="background: #28a745;">下載數據</a>
                    </div>
                    
                    <!-- 健康檢查 -->
                    <div class="endpoint-card">
                        <h3>❤️ 健康檢查</h3>
                        <div class="endpoint-path">GET /health</div>
                        <div class="endpoint-desc">
                            檢查服務和資料庫的健康狀態，確認一切正常運行。
                        </div>
                        <a href="/health" class="btn" target="_blank">測試此端點</a>
                    </div>
                    
                    <!-- API 文檔 -->
                    <div class="endpoint-card">
                        <h3>📖 API 文檔</h3>
                        <div class="endpoint-path">GET /docs</div>
                        <div class="endpoint-desc">
                            完整的 Swagger UI API 文檔，包含所有端點的詳細說明和測試功能。
                        </div>
                        <a href="/docs" class="btn" target="_blank">查看文檔</a>
                    </div>
                    
                    <!-- 個別數據端點 -->
                    <div class="endpoint-card">
                        <h3>🎥 影片數據</h3>
                        <div class="endpoint-path">GET /vlogs</div>
                        <div class="endpoint-desc">
                            取得所有影片紀錄數據，從 MongoDB 資料庫讀取。
                        </div>
                        <a href="/vlogs" class="btn" target="_blank">查看數據</a>
                    </div>
                    
                    <div class="endpoint-card">
                        <h3>😊 情緒數據</h3>
                        <div class="endpoint-path">GET /emotions</div>
                        <div class="endpoint-desc">
                            取得所有情緒評分數據，從 MongoDB 資料庫讀取。
                        </div>
                        <a href="/emotions" class="btn" target="_blank">查看數據</a>
                    </div>
                    
                    <div class="endpoint-card">
                        <h3>📍 GPS 數據</h3>
                        <div class="endpoint-path">GET /gps</div>
                        <div class="endpoint-desc">
                            取得所有位置數據，從 MongoDB 資料庫讀取。
                        </div>
                        <a href="/gps" class="btn" target="_blank">查看數據</a>
                    </div>
                </div>
                
                <!-- MongoDB 資訊 -->
                <h2 class="section-title">🗄️ MongoDB 資料庫資訊</h2>
                <div class="status-card">
                    <div class="status-icon">💾</div>
                    <div class="status-details">
                        <h2>資料庫配置</h2>
                        <p><strong>資料庫名稱：</strong>emogo_db</p>
                        <p><strong>集合數量：</strong>3 個 (vlogs, emotions, gps)</p>
                        <p><strong>數據來源：</strong>MongoDB Atlas</p>
                        <p><strong>連線狀態：</strong> {db_status}</p>
                        <a href="https://www.mongodb.com/cloud/atlas" class="btn btn-secondary" target="_blank">訪問 MongoDB Atlas</a>
                    </div>
                </div>
            </div>
            
            <!-- 頁尾 -->
            <div class="footer">
                <p><strong>EmoGo Backend API</strong> - 心理資訊學與神經資訊學課程作業</p>
                <p class="course-info">國立台灣大學 資訊工程學系 | Week 13 - FastAPI + MongoDB</p>
                <p class="course-info">洪于茹 (R14546007) | {datetime.now().strftime("%Y年%m月%d日 %H:%M")}</p>
            </div>
        </div>
    </body>
    </html>
    """

# 主要需求：匯出端點
@app.get("/export")
def export_all():
    """主要作業要求：從 MongoDB 提供三種類型數據"""
    try:
        # 從 MongoDB 取得所有數據
        vlogs = list(vlogs_collection.find({}, {"_id": 0}))
        emotions = list(emotions_collection.find({}, {"_id": 0}))
        gps = list(gps_collection.find({}, {"_id": 0}))
        
        response_data = {
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "student": "洪于茹",
                "student_id": "R14546007",
                "data_types": ["vlogs", "emotions", "gps"],
                "total_records": len(vlogs) + len(emotions) + len(gps),
                "assignment": "Week 13 - EmoGo Backend",
                "data_source": "MongoDB Atlas"
            },
            "data": {
                "vlogs": vlogs,
                "emotions": emotions,
                "gps": gps
            }
        }
        
        return JSONResponse(content=response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匯出失敗: {str(e)}")

# 新增：下載端點 - 專門提供檔案下載
@app.get("/download")
async def download_data():
    """下載所有數據為 JSON 檔案"""
    try:
        # 從 MongoDB 取得所有數據
        vlogs = list(vlogs_collection.find({}, {"_id": 0}))
        emotions = list(emotions_collection.find({}, {"_id": 0}))
        gps = list(gps_collection.find({}, {"_id": 0}))
        
        response_data = {
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "student": "洪于茹",
                "student_id": "R14546007",
                "data_types": ["vlogs", "emotions", "gps"],
                "total_records": len(vlogs) + len(emotions) + len(gps),
                "assignment": "Week 13 - EmoGo Backend",
                "data_source": "MongoDB Atlas"
            },
            "data": {
                "vlogs": vlogs,
                "emotions": emotions,
                "gps": gps
            }
        }
        
        # 直接回傳 JSONResponse，讓瀏覽器處理下載
        import json
        from fastapi.responses import JSONResponse
        
        # 建立 JSON 字串
        json_str = json.dumps(response_data, ensure_ascii=False, indent=2)
        
        # 建立回應
        from fastapi.responses import Response
        return Response(
            content=json_str,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=emogo_data.json"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下載失敗: {str(e)}")

# 健康檢查端點
@app.get("/health")
def health():
    """健康檢查，確認服務和資料庫狀態"""
    try:
        client.server_info()
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"

    # 檢查影片資料夾
    video_files = []
    if os.path.exists(VIDEO_DIR):
        video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EmoGo Backend API",
        "student": "洪于茹 (R14546007)",
        "assignment": "Week 13 - FastAPI + MongoDB",
        "database": db_status,
        "video_files": {
            "directory": VIDEO_DIR,
            "count": len(video_files),
            "files": video_files
        },
        "endpoints": {
            "home": "/",
            "export": "/export",
            "download": "/download",
            "health": "/health",
            "docs": "/docs",
            "vlogs": "/vlogs",
            "emotions": "/emotions",
            "gps": "/gps"
            "videos_list": "/videos",
            "video_download": "/videos/{video_id}"

        }
    }

# 各類型數據端點
@app.get("/vlogs")
def get_vlogs():
    """取得所有影片紀錄"""
    try:
        vlogs = list(vlogs_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        return {
            "count": len(vlogs),
            "data": vlogs,
            "type": "vlogs"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得影片數據失敗: {str(e)}")

@app.get("/emotions")
def get_emotions():
    """取得所有情緒數據"""
    try:
        emotions = list(emotions_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        return {
            "count": len(emotions),
            "data": emotions,
            "type": "emotions"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得情緒數據失敗: {str(e)}")

@app.get("/gps")
def get_gps():
    """取得所有 GPS 數據"""
    try:
        gps = list(gps_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        return {
            "count": len(gps),
            "data": gps,
            "type": "gps"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得 GPS 數據失敗: {str(e)}")

# 新增數據端點
@app.post("/vlogs")
def create_vlog(vlog: VlogData):
    """新增影片紀錄"""
    try:
        vlog_dict = vlog.dict()
        vlog_dict["timestamp"] = datetime.now().isoformat()
        result = vlogs_collection.insert_one(vlog_dict)
        vlog_dict.pop("_id", None)
        return {
            "message": "影片紀錄新增成功",
            "id": str(result.inserted_id),
            "data": vlog_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增影片紀錄失敗: {str(e)}")

@app.post("/emotions")
def create_emotion(emotion: EmotionData):
    """新增情緒數據"""
    try:
        emotion_dict = emotion.dict()
        emotion_dict["timestamp"] = datetime.now().isoformat()
        result = emotions_collection.insert_one(emotion_dict)
        emotion_dict.pop("_id", None)
        return {
            "message": "情緒數據新增成功",
            "id": str(result.inserted_id),
            "data": emotion_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增情緒數據失敗: {str(e)}")

@app.post("/gps")
def create_gps(gps: GPSData):
    """新增 GPS 數據"""
    try:
        gps_dict = gps.dict()
        gps_dict["timestamp"] = datetime.now().isoformat()
        result = gps_collection.insert_one(gps_dict)
        gps_dict.pop("_id", None)
        return {
            "message": "GPS 數據新增成功",
            "id": str(result.inserted_id),
            "data": gps_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增 GPS 數據失敗: {str(e)}")

# 應用程式啟動事件
@app.on_event("startup")
def startup_event():
    """啟動時初始化測試數據"""
    try:
        # 測試資料庫連線
        client.server_info()
        print("✅ MongoDB 連線成功")
        
        # 初始化測試數據（如果集合是空的）
        if vlogs_collection.count_documents({}) == 0:
            vlogs_collection.insert_many([
                {
                    "id": "vlog_001",
                    "description": "1-second video recording - Happy moment",
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                    "video_filename": "vlog_001.mp4",
                    "video_download_url": f"{BASE_URL}/videos/vlog_001"
                },
                {
                    "id": "vlog_002",
                    "description": "1-second video recording - Study session",
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                    "video_filename": "vlog_002.mp4",
                    "video_download_url": f"{BASE_URL}/videos/vlog_002"
                }
            ])
            print("✅ Vlogs 測試數據已插入（包含影片下載連結）")
        
        if emotions_collection.count_documents({}) == 0:
            emotions_collection.insert_many([
                {
                    "id": "emotion_001",
                    "sentiment": 4,
                    "scale": "1-5 (1=very bad, 5=very good)",
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                },
                {
                    "id": "emotion_002",
                    "sentiment": 5,
                    "scale": "1-5 (1=very bad, 5=very good)",
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                }
            ])
            print("✅ Emotions 測試數據已插入")
        
        if gps_collection.count_documents({}) == 0:
            gps_collection.insert_many([
                {
                    "id": "gps_001",
                    "latitude": 25.0170,
                    "longitude": 121.5395,
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                },
                {
                    "id": "gps_002",
                    "latitude": 25.0150,
                    "longitude": 121.5415,
                    "timestamp": datetime.now().isoformat(),
                    "student": "洪于茹",
                    "student_id": "R14546007"
                }
            ])
            print("✅ GPS 測試數據已插入")
            
    except Exception as e:
        print(f"❌ MongoDB 連線失敗: {e}")
# ========== 影片檔案下載端點 ==========
@app.get("/videos/{video_id}")
async def download_video_file(video_id: str):
    """
    下載實際的影片檔案
    範例：GET /videos/vlog_001 會下載 vlog_001.mp4
    這是老師要求的實際影片下載功能
    """
    try:
        # 檢查影片ID是否有效
        valid_videos = ["vlog_001", "vlog_002"]
        
        if video_id not in valid_videos:
            raise HTTPException(status_code=404, detail="影片ID不存在")
        
        # 影片檔案路徑
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(VIDEO_DIR, video_filename)
        
        # 檢查檔案是否存在
        if not os.path.exists(video_path):
            raise HTTPException(
                status_code=404, 
                detail=f"影片檔案未找到：{video_filename}"
            )
        
        # 檢查檔案大小
        file_size = os.path.getsize(video_path)
        
        print(f"📹 提供影片下載：{video_filename} ({file_size} bytes)")
        
        # 回傳影片檔案
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=video_filename,
            headers={
                "Content-Disposition": f"attachment; filename={video_filename}"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"影片下載失敗: {str(e)}")

# ========== 影片列表端點 ==========
@app.get("/videos")
async def list_videos():
    """
    列出所有可下載的影片
    """
    try:
        # 從資料庫取得所有影片資訊
        vlogs = list(vlogs_collection.find({}, {"_id": 0}))
        
        videos_list = []
        for vlog in vlogs:
            if "video_download_url" in vlog:
                videos_list.append({
                    "id": vlog["id"],
                    "description": vlog["description"],
                    "timestamp": vlog["timestamp"],
                    "download_url": vlog["video_download_url"],
                    "filename": vlog.get("video_filename", "")
                })
        
        return {
            "count": len(videos_list),
            "videos": videos_list,
            "message": f"使用 /videos/{{id}} 下載影片，例如：/videos/vlog_001"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得影片列表失敗: {str(e)}")
    
# ========== 影片檔案下載端點 ==========
@app.get("/videos/{video_id}")
async def download_video_file(video_id: str):
    """
    下載實際的影片檔案
    範例：GET /videos/vlog_001 會下載 vlog_001.mp4
    這是老師要求的實際影片下載功能
    """
    try:
        # 檢查影片ID是否有效
        valid_videos = ["vlog_001", "vlog_002"]
        
        if video_id not in valid_videos:
            raise HTTPException(status_code=404, detail="影片ID不存在")
        
        # 影片檔案路徑
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(VIDEO_DIR, video_filename)
        
        # 檢查檔案是否存在
        if not os.path.exists(video_path):
            raise HTTPException(
                status_code=404, 
                detail=f"影片檔案未找到：{video_filename}"
            )
        
        # 檢查檔案大小
        file_size = os.path.getsize(video_path)
        
        print(f"📹 提供影片下載：{video_filename} ({file_size} bytes)")
        
        # 回傳影片檔案
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=video_filename,
            headers={
                "Content-Disposition": f"attachment; filename={video_filename}"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"影片下載失敗: {str(e)}")

# ========== 影片列表端點 ==========
@app.get("/videos")
async def list_videos():
    """
    列出所有可下載的影片
    """
    try:
        # 從資料庫取得所有影片資訊
        vlogs = list(vlogs_collection.find({}, {"_id": 0}))
        
        videos_list = []
        for vlog in vlogs:
            if "video_download_url" in vlog:
                videos_list.append({
                    "id": vlog["id"],
                    "description": vlog["description"],
                    "timestamp": vlog["timestamp"],
                    "download_url": vlog["video_download_url"],
                    "filename": vlog.get("video_filename", "")
                })
        
        return {
            "count": len(videos_list),
            "videos": videos_list,
            "message": f"使用 /videos/{{id}} 下載影片，例如：/videos/vlog_001"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得影片列表失敗: {str(e)}")
           
# 應用程式關閉事件
@app.on_event("shutdown")
def shutdown_event():
    """關閉時關閉資料庫連線"""
    client.close()
    print("✅ MongoDB 連線已關閉")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)