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


class Modals(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    class SuggestionModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(timeout=None, delete_message_after=True)
            self.user_name = discord.ui.TextInput(label="Your Discord Username", placeholder="eg. cutepanda27", required=True, max_length=32)
            self.suggestion = discord.ui.TextInput(label="Title Your Suggestion", placeholder="eg. Add a leveling system to the bot.", required=True, max_length=1000)
            self.description = discord.ui.TextInput(label="Detail Your Suggestion", placeholder="Provide detailed information about your suggestion.", required=True, min_length=20)
            self.contact = discord.ui.TextInput(label="Can we contact you for further information?", placeholder="Yes, No.", required=True, max_length=20)

        async def callback(self, interaction: discord.Interaction):
            pass

        async def on_submit(self, interaction: discord.Interaction):
            server_id = 1185320952448430180
            thread_id = 1197529033567637514

            guild = self.client.get_guild(server_id)
            thread = discord.utils.get(guild.threads, id=thread_id)

            if thread:
                embed = discord.Embed(title=":bulb: New Suggestion", color=0xB19D30)
                embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
                embed.add_field(name=":newspaper2: Username", value=self.user_name.value, inline=False)
                embed.add_field(name=":identification_card: Suggestion Title", value=self.suggestion.value, inline=False)
                embed.add_field(name=":scroll: Description", value=self.description.value, inline=False)
                embed.add_field(name=":rotating_light: Receive Updates?", value=self.contact.value, inline=False)

                suggestion_message = await thread.send(embed=embed)
                await suggestion_message.add_reaction('<:greencheck:1209602728855085146>')
                await suggestion_message.add_reaction('<:redcross:1209602727328612532>')
                await interaction.response.send_message(f":love_letter: Thank you for submitting your suggestion! I have sent this to [**Strexify's Discord Server.**](https://discord.gg/fzkfvTytge) The bot management team will review it soon!", ephemeral=True)

                self.store_suggestion(interaction.user.id, self.user_name.value, self.suggestion.value, self.description.value, self.contact.value)
            else:
                await interaction.response.send_message("Sorry, I could not find the channel to send this suggestion.", ephemeral=True)

    suggestions_list = []

    def store_suggestion(self, user_id, user_name, suggestion_name, description, contact):
        self.suggestions_list.append({
            "user_id": user_id,
            "user_name": user_name,
            "suggestion_name": suggestion_name,
            "description": description,
            "contact": contact
        })

    @app_commands.command(name="suggest", description="Suggest a feature for the bot")
    async def suggestion_command(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.SuggestionModal())

    class BugModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(timeout=None, delete_message_after=True)
            self.user_name = discord.ui.TextInput(label="Your Discord Username", placeholder="eg. cutepanda27", required=True, max_length=32)
            self.bug = discord.ui.TextInput(label="Title Your Issue", placeholder="eg. Add a leveling system to the bot.", required=True, max_length=1000)
            self.description = discord.ui.TextInput(label="Detail Your Issue", placeholder="Provide detailed information about your issue.", required=True, min_length=20)
            self.contact = discord.ui.TextInput(label="Can we contact you for further information?", placeholder="Yes, No.", required=True, max_length=3, min_length=2)

        async def callback(self, interaction: discord.Interaction):
            pass

        async def on_submit(self, interaction: discord.Interaction):
            server_id = 1185320952448430180
            thread_id = 1198374894757482516

            guild = self.client.get_guild(server_id)
            thread = discord.utils.get(guild.threads, id=thread_id)

            if thread:
                embed = discord.Embed(title=":bug: Bug Report", color=0xB19D30)
                embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
                embed.add_field(name=":newspaper2: Username", value=self.user_name.value, inline=False)
                embed.add_field(name=":identification_card: Bug Title", value=self.bug.value, inline=False)
                embed.add_field(name=":scroll: Description", value=self.description.value, inline=False)
                embed.add_field(name=":rotating_light: Receive Updates?", value=self.contact.value, inline=False)

                embed.set_thumbnail(url=interaction.user.avatar.url)

                bug_message = await thread.send(embed=embed)
                await bug_message.add_reaction('<:greencheck:1209602728855085146>')
                await bug_message.add_reaction('<:redcross:1209602727328612532>')
                await interaction.response.send_message(f":love_letter: Thank you for submitting your issue! I have sent this to [**Strexify's Discord Server.**](https://discord.gg/fzkfvTytge) The bot management team will review it soon!", ephemeral=True)

                self.store_bug(interaction.user.id, self.user_name.value, self.bug.value, self.description.value)
            else:
                await interaction.response.send_message("Sorry, I could not find the channel to send this bug.", ephemeral=True)

    bug_list = []

    def store_bug(self, user_id, user_name, bug_name, description):
        self.bug_list.append({
            "user_id": user_id,
            "user_name": user_name,
            "bug_name": bug_name,
            "description": description
        })

    @app_commands.command(name="bugreport", description="Report a bug")
    async def bugreport(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.BugModal())

async def setup(client):
    await client.add_cog(Modals(client))
