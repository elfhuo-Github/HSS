import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Variable to track the previous Hyperspin status
previous_status = None

async def create_status_channel():
    # Get the default guild (the guild where the command was used)
    guild = bot.guilds[0]

    # Check if the channel already exists
    existing_channel = discord.utils.get(guild.channels, name='HyperSpin Status')

    if not existing_channel:
        # Channel doesn't exist, create it
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        new_channel = await guild.create_text_channel('HyperSpin Status', overwrites=overwrites)
        print(f"Created **HyperSpin Status** channel with ID {new_channel.id}")

    else:
        print(f"**HyperSpin Status** channel already exists with ID {existing_channel.id}")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    print(f'Connected to guilds: {", ".join([guild.name for guild in bot.guilds])}')

@bot.command(name='hyperspinstatus', help='Check Hyperspin download status.')
async def hyperspin_status(ctx):
    await check_hyperspin_status(ctx)

@bot.command(name='forcecheck', help='Force the bot to check Hyperspin status again.')
@commands.bot_has_permissions(send_messages=True)
async def force_check(ctx):
    await check_hyperspin_status(ctx)

if __name__ == '__main__':
    bot.run(TOKEN)
