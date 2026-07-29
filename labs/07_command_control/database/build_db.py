import sqlite3
import os

def build_database():
    # Thư mục database của Lab 7
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, "sqlite.db")
    
    print(f"Building database at: {db_path}...")
    
    # Kết nối và khởi tạo database vật lý
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Tạo bảng users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            gender TEXT
        );
    """)
    
    # 2. Xóa dữ liệu cũ (để rebuild sạch sẽ) và thêm dữ liệu mẫu
    cursor.execute("DELETE FROM users;")
    
    sample_data = [
        ('Alice', 'alice@example.com', 25, 'Nữ'),
        ('Bob', 'bob@example.com', 30, 'Nam'),
        ('Charlie', 'charlie@example.com', 35, 'Nam')
    ]
    
    cursor.executemany(
        "INSERT INTO users (name, email, age, gender) VALUES (?, ?, ?, ?);", 
        sample_data
    )
    
    conn.commit()
    conn.close()
    print("Database built and seeded successfully!")

if __name__ == "__main__":
    build_database()
