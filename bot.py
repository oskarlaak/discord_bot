import os
import dotenv
from discord.ext.commands import Bot

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_PREFIXES = ('.', '/', '!')
MyBot = Bot(command_prefix=BOT_PREFIXES)


@MyBot.command(aliases=['helloworld', 'hello'], pass_context=True)
async def hello_world(context):
    channel = context.channel
    await channel.send('Hello World')


@MyBot.event
async def on_message(message):
    username = str(message.author)[:-5]  # Removing #xxxx from username
    user_message = message.content

    if message.author == MyBot.user:
        user_type = 'Bot'
    else:
        user_type = 'User'

    print("{} '{}' said: {}".format(user_type, username, user_message))
    await MyBot.process_commands(message)


@MyBot.event
async def on_ready():
    print('Bot ready')
    print('---------')


MyBot.run(TOKEN)
