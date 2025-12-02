import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def test_mongodb_connection():
    # 完整的連接字串
    uri = "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.qoknrio.mongodb.net/?appName=Cluster0"
    
    print("="*60)
    print("🔄 Testing MongoDB Atlas Connection")
    print("="*60)
    print(f"URI: {uri}")
    print(f"Python version: {sys.version[:50]}")
    
    try:
        # 創建客戶端
        client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        
        # 測試連接
        print("\n🔍 Pinging database...")
        client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB Atlas!")
        
        # 列出資料庫
        print("\n📊 Listing databases...")
        databases = client.list_database_names()
        print(f"Found {len(databases)} databases")
        for db in databases[:5]:  # 顯示前5個
            print(f"  - {db}")
        
        # 使用我們的資料庫
        db_name = "emogo"
        db = client[db_name]
        print(f"\n📁 Using database: {db_name}")
        
        # 創建必要的集合
        collections = ["vlogs", "emotions", "gps"]
        existing = db.list_collection_names()
        
        for col in collections:
            if col not in existing:
                db.create_collection(col)
                print(f"  Created collection: {col}")
            else:
                print(f"  Collection exists: {col}")
        
        # 插入測試數據
        print("\n📝 Inserting test data...")
        test_data = {
            "vlogs": [{"test": "vlog_data", "assignment": "Week 13", "timestamp": "2024-12-02"}],
            "emotions": [{"test": "emotion_data", "assignment": "Week 13", "timestamp": "2024-12-02"}],
            "gps": [{"test": "gps_data", "assignment": "Week 13", "timestamp": "2024-12-02"}]
        }
        
        for col, data in test_data.items():
            result = db[col].insert_many(data)
            print(f"  Inserted {len(result.inserted_ids)} records into {col}")
        
        # 檢查數據數量
        print("\n📊 Data counts:")
        for col in collections:
            count = db[col].count_documents({})
            print(f"  {col}: {count} records")
        
        client.close()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! MongoDB is ready for EmoGo backend!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {type(e).__name__}: {str(e)}")
        print("\n⚠️ Troubleshooting:")
        print("1. Check Network Access is 0.0.0.0/0 in MongoDB Atlas")
        print("2. Verify password is correct")
        print("3. Check internet connection")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
