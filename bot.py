import os
import dotenv
from discord.ext.commands import Bot
import requests

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_PREFIXES = ('.', '/', '!')
MyBot = Bot(command_prefix=BOT_PREFIXES)


@MyBot.command(aliases=['hello_world', 'hello'], pass_context=True)
async def helloworld(context):
    channel = context.channel
    await channel.send('Hello World')


@MyBot.command(aliases=['save_image', 'send_image'], pass_context=True)
async def saveimage(context, URL, filename):
    print('Getting image file from URL...')
    response = requests.get(URL)
    if response.status_code == 200:
        with open('images/{}'.format(filename), 'wb') as out_file:  # Creates new file
            out_file.write(response.content)  # Saves image to file
            print("Successfully saved image named '{}'".format(filename))
    del response  # Gets rid of original file


@MyBot.command(aliases=['display_image', 'show_image'], pass_context=True)
async def displayimage(context, filename):  # Requires name without file extension (.xxx)
    channel = context.channel
    for f in os.listdir('images'):
        if f.startswith(filename):
            await MyBot.send_file(channel, 'images/{}'.format(f))
            break
    else:
        print("Could not find image named '{}' to display".format(filename))


@MyBot.command(aliases=['delete_all_images'], pass_context=True)
async def deleteall(context):
    for f in os.listdir('images'):
        if not f.startswith('.'):  # Ignores .gitkeep
            os.remove('images/{}'.format(f))
            print("Deleted file named '{}'".format(f))
    print('Cleared everything in images folder')


@MyBot.command(aliases=['delete_image'], pass_context=True)
async def deletesingle(context, filename):  # Requires full name
    for f in os.listdir('images'):
        if f == filename:
            os.remove('images/{}'.format(f))
            print("Deleted file named '{}'".format(f))
            break
    else:
        print("Could not find image named '{}' to delete".format(filename))


@MyBot.event
async def on_message(message):
    username = str(message.author)[:-5]  # Removing #xxxx from username
    user_message = message.content

    if message.author == MyBot.user:
        user_type = 'MyBot'
    else:
        user_type = 'User'

    print("{} '{}' said: {}".format(user_type, username, user_message))
    await MyBot.process_commands(message)


@MyBot.event
async def on_ready():
    print('Bot ready')
    print('---------')


MyBot.run(TOKEN)
