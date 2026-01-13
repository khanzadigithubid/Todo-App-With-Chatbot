import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection string
connection_string = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_klKz0pB4qaiQ@ep-young-dawn-a42wlho5-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

try:
    print("Attempting to connect to PostgreSQL database...")
    conn = psycopg2.connect(connection_string)
    print("Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Database version: {db_version[0]}")
    
    cursor.close()
    conn.close()
    print("Connection closed.")
    
except Exception as e:
    print(f"Error connecting to database: {e}")