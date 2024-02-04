import discord
import os
from discord.ext import commands

# enables the bot's intentions/permissions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# image path (temporarily stored locally)
m_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
image = m_path + '\m.path\DUCK.png'

bot = discord.Client(intents=intents)
results_message = "Did these results help you?"


class Commands(commands.Bot):
    def __init__(self, prefix):
        # super initializing for the discord bot commands
        commands.Bot.__init__(self, command_prefix=prefix, intents=intents)

        self.feedback_received = True
        self.read_message = False
        self.read_message_author_id = 0
        self.results_id = 0
        self.prefix = prefix

    @bot.event
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    @bot.event
    async def on_message(self, message):
        # if message is from the bot
        if message.author == self.user:
            if message.content == results_message:
                await message.add_reaction("✅")
                await message.add_reaction("❌")
                self.feedback_received = False
            else:
                return

        # if message is from the user
        if self.read_message:
            if self.read_message_author_id == message.author.id:
                await self.m_anaylze(message)

        else:
            await self.m_menu(message)

    async def m_menu(self, options):
        if options.content.startswith(self.prefix + 'help'):
            pass

            # to eventually be merged to read
        elif options.content.startswith(self.prefix + 'image'):
            await options.channel.send(file=discord.File(image))

            # reads the next message after the command
        elif options.content.startswith(self.prefix + 'read'):
            await self.m_read(options)

        elif options.content.startswith(self.prefix + 'prefix'):
            await self.m_prefix(options)

    async def m_help(self, guide):
        pass

    async def m_prefix(self, message):
        prefix = message.content.replace(self.prefix + 'prefix', '')

        if prefix.strip() == "":
            await message.channel.send("Please enter a valid prefix.")
            return

        self.prefix = prefix.strip(" ")
        await message.channel.send(f"**{self.prefix}** is the new prefix.")

    async def m_read(self, command):
        print(command.author.id)  # temporary

        self.read_message_author_id = command.author.id
        await command.channel.send(
            f"Okay {command.author.display_name}, what message would you like me to read?")
        self.read_message = True

    @bot.event
    async def on_reaction_add(self, reaction, react_user):
        if react_user == self.user:
            return

        # responds to user feedback reactions
        if reaction.message.content == results_message and not self.feedback_received:
            if reaction.emoji == "✅":
                await reaction.message.channel.send("Thanks for the feedback!")
                self.feedback_received = True

            elif reaction.emoji == "❌":
                await reaction.message.channel.send(
                    "Sorry to hear that. I'll try to do better next time!")
                self.feedback_received = True

    async def m_anaylze(self, message_to_anaylze):
        await message_to_anaylze.channel.send("Analyzing message...")
        message_content = message_to_anaylze.content  # stores/overwrites message temporarily

        # Code for reading the message content (TBC)

        await message_to_anaylze.channel.send(f"Results: {message_content}")

        # Code for showing results here (TBC)

        await message_to_anaylze.channel.send(results_message)
        self.read_message = False
