import os, discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

hello = "hello"
read_message = False
read_message_author_id = 0


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    

@bot.event
async def on_message(message):
    global read_message
    global read_message_author_id
    if message.author == bot.user:
        return
    

    if not(read_message):
        if message.content.startswith('m.read'):
            read_message_author_id = message.author.id
            print(message.author.id)
            message_author_name = message.author.display_name
            await message.channel.send(f"Ok {message_author_name}, what message would you like me to read?")
            read_message = True
    else:
        if (read_message_author_id == message.author.id):
            await message.channel.send("Ok, give me a little bit to analyze the message...")
            message_content = message.content
            # Put the code for reading the message content here
            await message.channel.send(f"Ok, here are the results: {message_content}")
            # Put the code for showing results here
            await message.channel.send("Did these results help you? React with a checkmark if yes, an X if no.")
            read_message = False

    
    




bot.run(TOKEN)
