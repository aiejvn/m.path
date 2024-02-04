import os
from commands import Commands
from dotenv import load_dotenv

# loads Discord bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# bot is created and run here
def main():
    my_prefix = input("Enter custom prefix: ")
    my_bot = Commands(my_prefix)

    my_bot.run(TOKEN)

main()

