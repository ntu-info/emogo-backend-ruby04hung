import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

print(f"Python version: {sys.version}")
print(f"PyMongo version: {sys.modules['pymongo'].__version__ if 'pymongo' in sys.modules else 'Not found'}")

# 測試連接
uri = "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.qoknrio.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # 檢查數據
    db = client["emogo"]
    print(f"📊 Database collections: {db.list_collection_names()}")
    
    for col in ["vlogs", "emotions", "gps"]:
        if col in db.list_collection_names():
            count = db[col].count_documents({})
            print(f"   {col}: {count} records")
    
    client.close()
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
