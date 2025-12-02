import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def test_connection():
    # 你的 MongoDB 連接字串
    uri = "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.gokuri.o.mongodb.net/?appName=Cluster0"
    
    print("🔗 Testing MongoDB Atlas connection...")
    print(f"URI: {uri}")
    
    try:
        # 創建客戶端
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=10000)
        
        # 測試連接
        print("Pinging database...")
        await client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB Atlas!")
        
        # 列出資料庫
        print("Listing databases...")
        databases = await client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        # 使用我們的資料庫
        db_name = "emogo"
        db = client[db_name]
        print(f"📁 Using database: {db_name}")
        
        # 創建集合（如果不存在）
        collections_needed = ["vlogs", "emotions", "gps"]
        existing_collections = await db.list_collection_names()
        
        for collection in collections_needed:
            if collection not in existing_collections:
                await db.create_collection(collection)
                print(f"   Created collection: {collection}")
            else:
                print(f"   Collection exists: {collection}")
        
        # 檢查數據數量
        print("\n📊 Checking data counts:")
        for collection in collections_needed:
            count = await db[collection].count_documents({})
            print(f"   {collection}: {count} records")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("\n⚠️ Troubleshooting steps:")
        print("1. Check Network Access in MongoDB Atlas is set to 0.0.0.0/0")
        print("2. Verify username and password are correct")
        print("3. Make sure cluster is running (status should be green)")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
