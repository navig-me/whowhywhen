import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secrect@142.93.220.56:5432/whowhywhendb")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200
STRIPE_PUBLISHABLE_KEY = "pk_live_51PU7s5C0V9GgAoCfCmGXtu12AufWh8cd6Isopm41b7FGlpcHiz9o0UwpXQ3d7xp39cteHdHjroHHHZ8wWEoaEZOn00CH8uRtqX"
STRIPE_SECRET_KEY = "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"
TURNSTILE_SECRET_KEY = "0x4AAAAAAAelvYaX_D2kAiR7VM2LnTwAwR4"
