import os, discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Client(intents=intents)

hello = "hello"
read_message = False
feedback_recieved = True
read_message_author_id = 0
results_message = "Did these results help you?"
 # Please react with :white_check_mark: if they did, or :x: if no. Feedback tells me if I'm doing a good job, or if I need to improve!
results_id = 0

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    

@bot.event
async def on_message(message):
    global read_message
    global read_message_author_id
    global feedback_recieved

    if message.author == bot.user:
        if message.content == results_message:
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            feedback_recieved = False
        else:
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
            print("Wow")
            #await message.channel.send("Ok, give me a little bit to analyze the message...")
            message_content = message.content
            # Put the code for reading the message content here
            await message.channel.send(f"Ok, here are the results: {message_content}")
            # Put the code for showing results here
            await message.channel.send(results_message)
            read_message = False

@bot.event
async def on_reaction_add(reaction, react_user):
    global feedback_recieved

    if react_user == bot.user:
        return
    if reaction.message.content == results_message and not feedback_recieved:
        if reaction.emoji == "✅":
            await reaction.message.channel.send("Thanks for the feedback! Glad to hear I did a good job!")
            feedback_recieved = True
        elif reaction.emoji == "❌":
            await reaction.message.channel.send("Sorry to hear that. I'll try to do better next time!")
            feedback_recieved = True

def main():
    bot.run(TOKEN)

main()
