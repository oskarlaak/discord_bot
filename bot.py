import discord
import dotenv
import os
from discord.ext.commands import Bot

dotenv.load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIXES = ('.', '/', '!')
MyBot = Bot(command_prefix = BOT_PREFIXES)

@MyBot.command(aliases = ['helloworld', 'hello'], pass_context = True)
async def hello_world(context):
    print('Hello World')

    channel = context.channel
    await channel.send('Hello World')

MyBot.run(TOKEN)
