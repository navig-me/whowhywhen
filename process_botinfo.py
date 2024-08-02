import json
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from app.config import DATABASE_URL
from app.models.apikey import APIKey
from app.models.apilog import APILog
from app.models.botinfo import BotInfo
from app.models.user import User, UserProject

# Create a SQLAlchemy session
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def clean_pattern(pattern):
    # Remove any leading or trailing whitespace
    pattern = pattern.strip()

    # Remove all characters that are not letters, digits, -, . or _
    pattern = ''.join(c for c in pattern if c.isalnum() or c in ('-', '.', '_'))

    return pattern

with open('user_agents.json', 'r') as f:
    # Load the JSON data
    data = json.load(f)

# Process the botinfo data
for bot in tqdm(data):
    # Extract the pattern and url from the bot
    pattern = bot.get('pattern')
    url = bot.get('url')
    name = clean_pattern(pattern)

    with get_session() as session:
        print("Processing bot info:", name)
        # Check if name is already in the database
        bot_info = session.execute(select(BotInfo).where(BotInfo.bot_name == name)).scalar_one_or_none()
        if bot_info:
            continue

        # Check if the pattern and url are present in the botinfo.json file
        if pattern and url:
            print("Adding bot info to the database...")
            bot_info = BotInfo(
                bot_name=name,
                website=url,
                pattern=pattern,
            )
            session.add(bot_info)
            session.commit()
            session.refresh(bot_info)

            # For all APILog where user_agent contains the regex pattern, update the bot_type ID
            api_logs = session.execute(select(APILog).where(APILog.user_agent.contains(pattern))).scalars().all()
            print("Adding bot type to API logs...", len(api_logs))
            for api_log in api_logs:
                api_log.bot_id = bot_info.id
                session.add(api_log)
            session.commit()
