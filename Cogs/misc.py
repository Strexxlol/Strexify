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
import time
import urllib


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []


    @commands.hybrid_command(name="sync", description="Sync the bot's slash commands")
    async def sync(self, ctx):
        await self.client.tree.sync()
        await ctx.reply("I have successfully synced all slash commands!", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

async def setup(client):
    await client.add_cog(Misc(client))
