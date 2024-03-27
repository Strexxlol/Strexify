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


class Partners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.hybrid_command(name="partners", description="Show partner information")
    async def partners(self, ctx):
        embed = discord.Embed(
            title="Partner Information",
            description="Click any button below for more details!",
            color=0xB19D30,
        )

        embed.set_thumbnail(
            url="https://emojiisland.com/cdn/shop/products/Handshake_Emoji_Icon_ios10_grande.png?v=1571606090"
        )

        view = discord.ui.View()

        async def harmony_button_callback(interaction: discord.Interaction):
            response_embed = discord.Embed(
                title="Harmony",
                description="""Introducing Harmony – your all-in-one solution for Discord server management! 🎉

                Say goodbye to clutter and hello to streamlined perfection with Harmony! This top-notch bot is designed to elevate your Discord experience to new heights, all while keeping things simple and seamless. 🚀

                Powered by JavaScript and built on the robust Discord.js V14.0.0 framework, Harmony brings a plethora of premium features right to your fingertips. From moderation tools to info-related commands, fun games which are amazing, and even a collection of hilarious jokes, Harmony has it all! 👾

                Why juggle multiple bots when you can have everything you need in one harmonious package? With Harmony, managing your server has never been easier – it's like having your very own Swiss Army knife for Discord! 🔧

                So why wait? Dive into the ultimate Discord experience today and let Harmony save the day! After all, why settle for discord when you can have harmony? 😉\n- [Invite me!](https://discord.com/oauth2/authorize?client_id=1212354495103897671&permissions=8&scope=bot)""",
                color=0xB19D30,
            )
            response_embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/1212354495103897671/a_ea04df562b095925d2deecec1959f9c4.gif?"
            )
            await interaction.response.send_message(
                embed=response_embed, ephemeral=True
            )

        async def jaggededge_button_callback(interaction: discord.Interaction):
            response_embed = discord.Embed(
                title="JaggedEdge", description="test working?", color=0xFF0000
            )
            response_embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/1190684779738312764/5f581a607ad45a0e7184f263f9263e59.png?"
            )
            await interaction.response.send_message(
                embed=response_embed, ephemeral=True
            )

        async def sharded_button_callback(interaction: discord.Interaction):
            response_embed = discord.Embed(
                title="Sharded",
                description="""The bot, that is focused on *simplifying Discord*

                The current version of Discord knows a lot of features, and a lot of bots. Our main purpose with Sharded, is to make it easier to manage (large) servers.

                With Sharded having one main task, to be the one bot every server needs
                **How?** By creating all the commands that are mainly used in many servers, and *combine them into one bot.*

                You can check out all features in our server.
                We also offer coding help (focused on Discord bots, written with the **discord.py** / **nextcord.py** library)
                You can also find tutorials on how to start a Discord bot yourself!
                *Not interested in coding?* We also offer a chill launch and if you have a question, related to anything, we'll help!\n\n- Interested? Join the [Discord Server](https://discord.gg/BVGB3yXS3z)""",
                color=0xE31CDC,
            )
            response_embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/982312573179396106/c8feb0f79de983d9fa41bd69e9925e1a.png?size=1024"
            )
            await interaction.response.send_message(
                embed=response_embed, ephemeral=True
            )

        async def silentars_button_callback(interaction: discord.Interaction):
            response_embed = discord.Embed(
                title="SilentARS",
                description="""SilentARS is a Discord Bot that is designed to help you build a fun and healthy community!

                SilentARS can do many many things, like tickets, giveaways, memes, and most importantly, it has AutoMod which you can setup using !automod-setup-now to block 99% of the hateful and dirty speech.\n\n- [Join me!](https://discord.gg/xzgjVp86Xz)""",
                color=0x5865F2,
            )
            response_embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/1200564877874434078/a_bf8bca47e25444549598a92dd0c00731.gif"
            )
            await interaction.response.send_message(
                embed=response_embed, ephemeral=True
            )

        button_harmony = discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="Harmony",
            emoji="<:harmony:1222151938414612623>",
        )
        button_harmony.callback = harmony_button_callback

        button_jaggededge = discord.ui.Button(
            style=discord.ButtonStyle.red,
            label="JaggedEdge",
            emoji="<:jagCool:1212381212619055145>",
        )
        button_jaggededge.callback = jaggededge_button_callback

        button_sharded = discord.ui.Button(
            style=discord.ButtonStyle.red,
            label="Sharded",
            emoji="<:Sharded:1212797652626968586>",
        )
        button_sharded.callback = sharded_button_callback

        button_silentars = discord.ui.Button(
            style=discord.ButtonStyle.blurple,
            label="SilentARS",
            emoji="<a:silentars:1221926167897178215>",
        )
        button_silentars.callback = silentars_button_callback

        view.add_item(button_harmony)
        view.add_item(button_jaggededge)
        view.add_item(button_sharded)
        view.add_item(button_silentars)

        await ctx.send(embed=embed, view=view)


async def setup(client):
    await client.add_cog(Partners(client))
