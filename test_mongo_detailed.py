import asyncio
import sys

async def test_mongodb_detailed():
    # 測試不同格式的連接字串
    uris_to_test = [
        # 格式1：基本格式
        "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.gokuri.o.mongodb.net/",
        
        # 格式2：帶參數
        "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.gokuri.o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        
        # 格式3：指定資料庫
        "mongodb+srv://ruby04hung_db_user:5x80COx9fuhB4KAk@cluster0.gokuri.o.mongodb.net/emogo?retryWrites=true&w=majority&appName=Cluster0"
    ]
    
    for i, uri in enumerate(uris_to_test, 1):
        print(f"\n{'='*60}")
        print(f"Test #{i}: {uri[:50]}...")
        print(f"{'='*60}")
        
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            # 設定較長的超時時間
            client = AsyncIOMotorClient(
                uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000
            )
            
            # 測試連接
            print("Pinging database...")
            await client.admin.command('ping')
            print("✅ Connection successful!")
            
            # 列出資料庫
            databases = await client.list_database_names()
            print(f"📊 Databases found: {len(databases)}")
            
            # 測試寫入
            db = client["test_db"]
            collection = db["test_collection"]
            result = await collection.insert_one({"test": "connection", "timestamp": "now"})
            print(f"📝 Test document inserted: {result.inserted_id}")
            
            # 刪除測試數據
            await collection.delete_many({})
            print("🧹 Test data cleaned up")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed: {type(e).__name__}: {str(e)[:100]}")
            continue
    
    return False

async def main():
    print("🔍 Starting MongoDB connection tests...")
    print(f"Python version: {sys.version}")
    
    try:
        import motor
        print(f"✅ Motor version: {motor.__version__}")
    except ImportError as e:
        print(f"❌ Motor not installed: {e}")
        print("Run: pip install motor pymongo")
        return False
    
    success = await test_mongodb_detailed()
    
    if success:
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! MongoDB connection is working!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ ALL TESTS FAILED. Please check:")
        print("1. Network Access in MongoDB Atlas (0.0.0.0/0)")
        print("2. Username and password")
        print("3. Internet connection")
        print("="*60)
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
