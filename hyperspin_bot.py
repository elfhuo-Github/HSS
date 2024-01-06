import discord
import os
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_website.start()

@tasks.loop(minutes=10)  # Check every 10 minutes, adjust as needed
async def check_website():
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.channels, name='downloads-status')  # Replace with your desired channel name

    url = 'https://www.hyperspin-fe.com/'  # HyperSpin homepage URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        message = soup.get_text()

        if 'Unfortunately, we had to take download section back offline' in message:
            status = 'Down'
            await update_notification(status, channel)
        else:
            status = 'Up'

        await channel.send(f'HyperSpin Downloads Page Status: {status}')
    else:
        await channel.send('Failed to retrieve HyperSpin Downloads Page status.')

async def update_notification(status, channel):
    if status == 'Down':
        await channel.send('Attention! The HyperSpin Downloads Page is currently down.')
    elif status == 'Up':
        await channel.send('Good news! The HyperSpin Downloads Page is back up and running.')

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='checkstatus')
async def check_status(ctx):
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.channels, name='downloads-status')  # Replace with your desired channel name

    url = 'https://www.hyperspin-fe.com/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        message = soup.get_text()

        if 'Unfortunately, we had to take download section back offline' in message:
            status = 'Down'
            await update_notification(status, channel)
        else:
            status = 'Up'

        await channel.send(f'Manual Check - HyperSpin Downloads Page Status: {status}')
    else:
        await channel.send('Failed to retrieve HyperSpin Downloads Page status for manual check.')

bot.run(TOKEN)
