load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

m_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

image = m_path + '\m.path\DUCK.png'

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
        if message.content.startswith('m.image'):
            await message.channel.send(file=discord.File(image))

        if message.content.startswith('m.read'):
            await m_read(message)
    else:
        if (read_message_author_id == message.author.id):
            await m_anaylze(message)


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


async def m_read(command):
    global read_message
    global read_message_author_id

    read_message_author_id = command.author.id
    print(command.author.id)
    message_author_name = command.author.display_name
    await command.channel.send(f"Ok {message_author_name}, what message would you like me to read?")
    read_message = True

async def m_anaylze(message_to_anaylze):
    global read_message 
    print("Wow")
    await message_to_anaylze.channel.send("Ok, give me a little bit to analyze the message...")
    message_content = message_to_anaylze.content

    # Put the code for reading the message content here

    await message_to_anaylze.channel.send(f"Ok, here are the results: {message_content}")
   
    # Put the code for showing results here

    await message_to_anaylze.channel.send(results_message)
    read_message = False

def main():
    bot.run(TOKEN)

main()
