from dotenv import load_dotenv
import os
load_dotenv()
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")