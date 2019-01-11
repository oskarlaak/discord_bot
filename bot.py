import os
import dotenv
from discord.ext.commands import Bot
import requests

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_PREFIXES = ('.', '/', '!')
MyBot = Bot(command_prefix=BOT_PREFIXES)


@MyBot.command(aliases=['helloworld', 'hello'], pass_context=True)
async def hello_world(context):
    channel = context.channel
    await channel.send('Hello World')


@MyBot.command(aliases=['save_image'], pass_context=True)
async def saveimage(context, URL, filename):
    response = requests.get(URL)
    if response.status_code == 200:
        with open('images/{}'.format(filename), 'wb') as out_file:  # Creates new file
            out_file.write(response.content)  # Saves image to file
    del response  # Gets rid of original file


@MyBot.command(aliases=['display_image'], pass_context=True)
async def displayimage(context, filename):
    channel = context.channel
    for f in os.listdir('images'):
        if f.startswith(filename):
            await MyBot.send_file(channel, 'images/{}'.format(f))
            break
    else:
        await channel.send('Could not find requested image')


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
