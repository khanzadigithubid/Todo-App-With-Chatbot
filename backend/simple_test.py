import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from env: {DATABASE_URL}")

# Check if it contains the problematic neon.tech URL
if DATABASE_URL and 'neon.tech' in DATABASE_URL:
    print("Detected Neon PostgreSQL URL")

    # Test if psycopg2 is available
    try:
        import psycopg2
        print("psycopg2 is available")
    except ImportError:
        print("psycopg2 is not available - this might be the issue")

    # Test if we can parse the URL
    try:
        from urllib.parse import urlparse
        parsed = urlparse(DATABASE_URL)
        print(f"Parsed successfully: scheme={parsed.scheme}, hostname={parsed.hostname}")
    except Exception as e:
        print(f"Failed to parse URL: {e}")
else:
    print("Using fallback database URL")