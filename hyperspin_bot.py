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

    # Check if the category already exists, or create it
    category_name = 'Hyperspin Status'
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        print(f"Created category **{category_name}** with ID {category.id}")

    # Check if the channel already exists
    channel_name = 'HyperSpin Status'
    existing_channel = discord.utils.get(category.channels, name=channel_name)

    if not existing_channel:
        # Channel doesn't exist, create it
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        new_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
        print(f"Created **{channel_name}** channel with ID {new_channel.id} in category {category.name}")

    else:
        print(f"**{channel_name}** channel already exists with ID {existing_channel.id} in category {category.name}")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    print(f'Connected to guilds: {", ".join([guild.name for guild in bot.guilds])}')

    # Get the default guild where the command was used
    guild = bot.guilds[0]

    if guild:
        # Create channels if not exist
        await create_status_channel()
    else:
        print("Error: Default guild not found.")

@bot.command(name='hyperspinstatus', help='Check Hyperspin download status.')
async def hyperspin_status(ctx):
    await check_hyperspin_status(ctx)

@bot.command(name='forcecheck', help='Force the bot to check Hyperspin status again.')
@commands.bot_has_permissions(send_messages=True)
async def force_check(ctx):
    await check_hyperspin_status(ctx)

if __name__ == '__main__':
    bot.run(TOKEN)
