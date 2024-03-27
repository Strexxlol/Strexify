# ✨ Welcome to Strexify - The Ultimate Solution!
# 💎 This repository contains the source code for Strexify!
# 🎁 Make sure you have the latest version of Python installed!
# 🎀 Join https://discord.gg/CvXyhbdmWv for any questions!

# 🛒 Importing necessary packages and modules
import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord import TextChannel
import humanize
from datetime import datetime as dt, timedelta
import asyncio
import random
from discord import ui, app_commands
import json
import datetime
from typing import Dict
from discord import ui
from typing import Union
import datetime as dt
import os
import tracemalloc
import sqlite3
import time
import requests
import time
import urllib
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)
tracemalloc.start()

# 📚 Setting up intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix='=', intents=intents)
client.remove_command('help')

# 🔧 Setting up the bot's status
bot_status = cycle([
    "Your All-in-One solution 💖",
    "Spying on {user_count} users 👀",
    "Strexifying {guild_count} servers 📢",
    "Get serious. Get Strexify ✨",
    "Power up with Strexify ⚡",
    "strexify.xyz 🔗"
])

# 🌐 Setting up the status cycle
@tasks.loop(seconds=5)
async def change_status():
    guild_count = len(client.guilds)
    user_count = sum(len(guild.members) for guild in client.guilds)
    game_name = next(bot_status).format(guild_count=guild_count, user_count=user_count)
    activity = discord.CustomActivity(name=game_name)
    await client.change_presence(activity=activity)

# 🌐 What shall happen once the bot runs?
@client.event
async def on_ready():
    print(Fore.CYAN + "---------------------------------------------")
    print(Fore.MAGENTA + Style.BRIGHT + "Bot is now online! Thanks for using Strexify!")
    print(Fore.CYAN + "---------------------------------------------")
    client.startTime = datetime.datetime.utcnow()
    change_status.start()
    await client.tree.sync()

@client.event
async def setup_hook():
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'Cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")

client.run("token")
