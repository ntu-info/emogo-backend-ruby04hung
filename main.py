from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# 作業要求的三種數據
data = {
    "vlogs": [
        {
            "id": "vlog_001",
            "description": "1-second video recording from EmoGo app",
            "timestamp": datetime.now().isoformat(),
            "student": "洪于茹",
            "student_id": "R14546007"
        }
    ],
    "emotions": [
        {
            "id": "emotion_001",
            "sentiment": 4,
            "scale": "1-5 (1=very bad, 5=very good)",
            "timestamp": datetime.now().isoformat(),
            "student": "洪于茹",
            "student_id": "R14546007"
        }
    ],
    "gps": [
        {
            "id": "gps_001",
            "latitude": 25.0170,
            "longitude": 121.5395,
            "timestamp": datetime.now().isoformat(),
            "student": "洪于茹",
            "student_id": "R14546007"
        }
    ]
}

@app.get("/")
def root():
    return {
        "app": "EmoGo Backend API",
        "assignment": "Week 13 - FastAPI + MongoDB",
        "student": "洪于茹 (R14546007)",
        "course": "Psychoinformatics & Neuroinformatics",
        "endpoints": {
            "home": "/",
            "export": "/export (MAIN REQUIREMENT)",
            "health": "/health"
        }
    }

@app.get("/export")
def export_all():
    """主要作業要求：提供三種類型數據"""
    return {
        "metadata": {
            "export_time": datetime.now().isoformat(),
            "student": "洪于茹",
            "student_id": "R14546007",
            "data_types": ["vlogs", "emotions", "gps"],
            "total_records": 3,
            "assignment": "Week 13 - EmoGo Backend"
        },
        "data": data
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
