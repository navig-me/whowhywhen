import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://doadmin:AVNS_OE93j-tOF5jRFWeEC37@wwwcluster-do-user-9035471-0.f.db.ondigitalocean.com:25060/wwwdb?sslmode=require")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200
STRIPE_PUBLISHABLE_KEY = "pk_live_51PU7s5C0V9GgAoCfCmGXtu12AufWh8cd6Isopm41b7FGlpcHiz9o0UwpXQ3d7xp39cteHdHjroHHHZ8wWEoaEZOn00CH8uRtqX"
STRIPE_SECRET_KEY = "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"
TURNSTILE_SECRET_KEY = "0x4AAAAAAAelvYaX_D2kAiR7VM2LnTwAwR4"

GOOGLE_CLIENT_ID = "209311359644-gj97vlisirrf64jc3cp11fpf2m8ojd61.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/dashauth/oauth2callback"

VAPID_PRIVATE_KEY = "v65uOwouU3f4DMjil1GbOB-n-wWnBUUZUaD1mgjEF58"
VAPID_PUBLIC_KEY = "BCaXWkZFN67uHxHaX1-o4Cwbd1k-G3o4Xo173mVuFFqwSbyKk9ywVhqn8G4LYZp7rksyx8-OafETKQA-hHaO3jY"