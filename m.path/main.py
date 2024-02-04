import os
from commands import Commands
from dotenv import load_dotenv

# loads Discord bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    my_bot = Commands()
    my_bot.run(TOKEN)

main()
