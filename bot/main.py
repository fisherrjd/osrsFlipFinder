from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#STEP 0 load token from somwhere safe

load_dotenv()
TOKEN = FINAL[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)