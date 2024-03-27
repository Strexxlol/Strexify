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

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.command_log.append((ctx.command.name, ctx.author.name))

        if len(self.command_log) > 50:
            self.command_log.pop(0)

    @commands.hybrid_group(name="role")
    async def role(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f"Hey there! Please use one of my following: `/role add`, `/role remove` or `/role replace`.")
      
            
    @role.command(name="add", description="Add roles to any user")
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            if ctx.me.top_role > role and ctx.author.top_role > role:
                await member.add_roles(role)
                await ctx.reply(f'Added `{role.name}` to `{member.display_name}`.', allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("You or the bot don't have sufficient permissions to add this role.", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.reply("I don't have permission to add roles.", allowed_mentions=discord.AllowedMentions.none())

    @role.command(name="remove", description="Revoke roles from any user")
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            if ctx.me.top_role > role and ctx.author.top_role > role:
                await member.remove_roles(role)
                await ctx.reply(f'Removed `{role.name}` from `{member.display_name}`.', allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("You or the bot don't have sufficient permissions to remove this role.", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.reply("I don't have permission to remove roles.", allowed_mentions=discord.AllowedMentions.none())

    @role.command(name="replace", description="Pick any user's role and replace it with a new one")
    async def replacerole(self, ctx, member: discord.Member, old_role: discord.Role, new_role: discord.Role):
        try:
            if ctx.me.guild_permissions.manage_roles and ctx.author.guild_permissions.manage_roles:
                if old_role in member.roles:
                    await member.remove_roles(old_role)
                    await member.add_roles(new_role)
                    await ctx.reply(f'Replaced `{old_role.name}` with `{new_role.name}` for **{member.display_name}**.', allowed_mentions=discord.AllowedMentions.none())
                else:
                    await ctx.reply(f'**{member.display_name}** does not have the `{old_role.name}` role.', allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("You or the bot don't have permission to manage roles.", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.reply("I don't have permission to manage roles.", allowed_mentions=discord.AllowedMentions.none())

            await ctx.send("I don't have permission to manage roles.")

    @commands.hybrid_group(name="nick")
    async def nick(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f"Hey there! Please use one of my following: `/role add`, `/role remove` or `/role replace`.")

    @nick.command(name="set", description="Change the nickname of any user")
    async def nickname(self, ctx, member: discord.Member, *, nickname: str):
        try:
            if ctx.me.guild_permissions.manage_nicknames and ctx.author.guild_permissions.manage_nicknames:
                await member.edit(nick=nickname)
                await ctx.send(f'Changed nickname of `{member.display_name}` to `{nickname}`.')
            else:
                await ctx.send("You or the bot don't have permission to change nicknames.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to change nicknames.")       
            
    @nick.command(name="reset", description="Reset anyone's server nickname")
    async def reset_nick(self,ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_nicknames:
            try:
                await member.edit(nick=None)
                await ctx.send(f"Nickname for {member.display_name} has been reset.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to reset the nickname.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @commands.hybrid_group(name="channel")
    async def channel(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f"Hey there! Please use one of my following: `/channel lock`, `/channel unlock` or `/channel rename`.")

    @channel.command(name="lock", description="Prevent members from speaking in a channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, duration: str = None, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        if channel.overwrites_for(ctx.guild.default_role).send_messages is False:
            await ctx.send(f"{channel.mention} is already locked.")
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"{channel.mention} has been locked. Members cannot speak there.")

        if duration:
            duration = duration.lower()
            time_units = {"m": 60, "h": 3600, "d": 86400, "s": 1}
            unit = duration[-1]
            if unit in time_units:
                try:
                    time = int(duration[:-1]) * time_units[unit]
                    await asyncio.sleep(time)
                    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    await ctx.send(f"{channel.mention} has been unlocked. Members can speak there again.")
                except ValueError:
                    await ctx.send("Invalid duration format.")
            else:
                await ctx.send("Invalid duration unit. Use 'm' for minutes, 'h' for hours, 'd' for days, or 's' for seconds.")

    @lock.error
    async def lock_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to lock channels.")
        else:
            await ctx.send("An error occurred while trying to lock the channel.")

    @channel.command(name="unlock", description="Unlocks the specified channel or the current locked channel, allowing members to speak again")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        if channel.overwrites_for(ctx.guild.default_role).send_messages is True:
            await ctx.send(f"{channel.mention} is already unlocked.")
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"{channel.mention} has been unlocked. Members can speak there again.")

    @unlock.error
    async def unlock_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to unlock channels.")
        else:
            await ctx.send("An error occurred while trying to unlock the channel.")   

    @channel.command(name="rename", description="Rename any channel or category")
    async def rename(self, ctx, target: discord.abc.GuildChannel, new_name: str):
        try:
            await target.edit(name=new_name)
            await ctx.send(f"Successfully renamed {target.mention} to it's new name!", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.send("I don't have the necessary permissions to rename channels.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())  

    @commands.hybrid_command(name="ban", description="Ban any user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await ctx.reply(f"{member.display_name} has been banned. Reason: {reason}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name='banlist', aliases=['blist'], description='Displays the list of banned members')
    async def banlist(self, ctx, user: discord.Member = None):
        ban_list = [ban_entry.user.name async for ban_entry in ctx.guild.bans()]

        embed = discord.Embed(title=':tools: Banned Members', color=0xB19D30)

        embed.set_thumbnail(url=ctx.guild.icon.url)

        if ban_list:
            for username in ban_list:
                banned_member = discord.utils.get(ctx.guild.members, name=username)
                if banned_member:
                    user_id = banned_member.id
                    embed.add_field(name=f'**{username} - ({user_id})**', value='\u200b', inline=False)
                else:
                    embed.add_field(name=f'**{username}**', value='\u200b', inline=False)
        else:
            embed.add_field(name='No Banned Members', value='There are no members banned in this server.')

        if user is not None:
            if user.id in [ban_entry.user.id for ban_entry in ctx.guild.bans()]:
                embed.add_field(name=f'{user.name} is banned', value='\u200b', inline=False)
            else:
                embed.add_field(name=f'{user.name} is not banned', value='\u200b', inline=False)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="purge", description="Delete a certain amount of messages", aliases=["clear", "delete"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int, user: commands.MemberConverter = None):
        def check(message):
            return user is None or message.author == user
        
        await ctx.channel.purge(limit=count + 1, check=check)

    @commands.hybrid_command(name="clearwarnings", description="Clear any user's server warnings")
    @commands.has_permissions(kick_members=True)
    async def clearwarnings(self, ctx, member: discord.Member):
        warnings = self.load_warnings()
        user_id = str(member.id)

        if user_id in warnings:
            del warnings[user_id]
            self.save_warnings(warnings)

            await ctx.reply(f"All warnings for {member.mention} have been cleared.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        else:
            await ctx.reply(f"{member.mention} has no warnings to clear.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    def save_warnings(self, warnings):
        with open("warnings.json", "w") as f:
            json.dump(warnings, f)

    def load_warnings(self):
        try:
            with open("warnings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @commands.hybrid_command(name="dm", description="Use the bot to send a direct message to a user")
    @commands.has_permissions(manage_messages=True)
    async def dm(self, ctx, user: discord.User, *, message: str):
        try:
            embed = discord.Embed(
                title="📝 You've received a message!",
                description = f"Sent from {ctx.author.mention} | `{ctx.author.id}`.",
                color=0xB19D30
            )

            embed.add_field(name=f"Message Content", value=f"```{message}```", inline=False)

            embed.set_footer(text=f"Message received from the following server: {ctx.guild.name}")

            await user.send(embed=embed)

            await ctx.send(f"💌 I have sent the following message to {user.name}:", embed=embed, ephemeral=True)
        except discord.Forbidden:
            await ctx.send("❗ Whoopsies! This user does not allow Direct messages.", ephemeral=True)

    @commands.hybrid_command(name="id", description="Get the ID of a user or role")
    async def id(self, ctx, target: discord.User = None, role: discord.Role = None):
        try:
            if target:
                embed = discord.Embed(
                    title="💳 User ID",
                    description=f"**The ID of user {target.display_name} is**\n`{target.id}`",
                    color=0xB19D30
                )

                embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/512/245/245266.png")

                await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            elif role:
                embed = discord.Embed(
                    title="💳 Role ID",
                    description=f"**The ID of role {role.name} is**\n{role.id}",
                    color=0xB19D30
                )

                embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/512/245/245266.png")

                await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("Please mention a user or provide a role to get the ID.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="kick", description="Kick any member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        await ctx.reply(f'Successfully kicked {member.mention}.', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="log", description="Get a log of the last 50 commands used")
    async def log(self, ctx):
        try:
            embed = discord.Embed(
                title="📝 Command Log",
                color=0xB19D30,
            )

            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5139/5139731.png")

            for command, user in self.command_log:
                embed.add_field(
                    name=f"{user}", 
                    value=f"`/{command}`", 
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.hybrid_command(name="mute", description="Prevent any user from sending messages")
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.manage_roles:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False)

            await member.add_roles(muted_role, reason=reason)
            await ctx.reply(f":mute: {member.mention} has been muted.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        else:
            await ctx.reply("You do not have the required permissions to use this command.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())   

    @commands.hybrid_command(name="unban", description="Unbans a user from the server (Use their user ID)")
    @app_commands.describe(user_id='The user ID of the banned user')
    async def unban(self, ctx, user_id: int):
        try:
            await ctx.guild.unban(discord.Object(id=user_id))

            await ctx.reply(f'Successfully unbanned user with ID {user_id}.', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        except discord.HTTPException as e:
            await ctx.reply(f'Failed to unban user with ID {user_id}. Error: {e}', mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="unmute", description="Allow any user to send messages after muting them")
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            if muted_role and muted_role in member.roles:
                await member.remove_roles(muted_role)
                await ctx.reply(f":speech_balloon: {member.mention} has been unmuted.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply(f":mute: I cannot unmute {member.mention} as he has not been muted.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        else:
            await ctx.reply("Sorry! You do not have the required permissions to use this command.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())                

async def setup(client):
  await client.add_cog(Moderation(client))