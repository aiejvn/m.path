import discord
import os
from discord.ext import commands
from new_nlp_algo import detect_emotion
from discord.ext.commands import has_permissions

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
    def __init__(self):
        # super initializing for the discord bot commands
        commands.Bot.__init__(self, command_prefix="em.", intents=intents)

        self.feedback_received = True
        self.read_message = False
        self.read_message_author_id = 0
        self.results_id = 0
        self.prefix = "em."

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
            pass

        else:
            await self.m_menu(message)

    async def m_menu(self, options):
        if options.content.startswith(self.prefix + 'help'):
            await self.m_help(options)

            # to eventually be merged to read
        elif options.content.startswith(self.prefix + 'image'):
            await options.channel.send(file=discord.File(image))

            # reads the next message after the command
        elif options.content.startswith(self.prefix + 'read'):
            await options.delete()
            await self.m_read(options)

        elif options.content.startswith(self.prefix + 'prefix'):
            await self.m_prefix(options)

    async def m_help(self, options):
        await options.author.send(f"*:･ﾟ✧*:･ﾟ✧ \nYou can summon me with the prefix {self.prefix} ! \n \n"
                                  f"**{self.prefix}read**: analyzes previous message. \n"
                                  f"**{self.prefix}prefix**: change default prefix. \n"
                                  f"**{self.prefix}help**: I will DM you a help guide. I am always here to guide you!")

    async def m_prefix(self, message):
        if not message.author.guild_permissions.administrator:
            await message.channel.send("Sorry, you do not have access to this command!")
            return

        prefix = message.content.replace(self.prefix + 'prefix', '')

        if prefix.strip() == "":
            await message.channel.send("Please enter a valid prefix.")
            return

        self.prefix = prefix.strip(" ")
        await message.channel.send(f"**{self.prefix}** is the new prefix.")

    async def m_read(self, command):
        self.read_message_author_id = command.author.id

        messages = [m async for m in command.channel.history(limit=1)]
        await self.m_anaylze(messages[0])

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
        print(message_content)

        # reads the message content
        results = detect_emotion(message_content)
        emotion_ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)

        if f"{emotion_ranked[0][1]:.3f}" == "0.000":
            await message_to_anaylze.channel.send(f"Sorry, human emotions are rather complicated and require more input"
                                                  f" data. I am currently not too sure what that message implies!")

            self.read_message = False
            return

        await message_to_anaylze.channel.send(f"Analyzed message is likely: \n \
            {emotion_ranked[0][0]}: {emotion_ranked[0][1]:.3f}\n \
            {emotion_ranked[1][0]}: {emotion_ranked[1][1]:.3f}\n \
            {emotion_ranked[2][0]}: {emotion_ranked[2][1]:.3f}")

        await message_to_anaylze.channel.send(results_message)
        self.read_message = False
