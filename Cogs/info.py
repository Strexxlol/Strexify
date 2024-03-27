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
import requests

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.client.startTime = datetime.datetime.utcnow()

    @commands.hybrid_command(name="avatar", description="Check any user's avatar", aliases=["icon", "pfp"])
    async def avatar(self, ctx, member: discord.Member=None):
        member = ctx.author if not member else member
        avatar_url = member.avatar.url
        
        embed = discord.Embed(title=member.display_name + "'s avatar", color=0xB19D30)
        embed.set_image(url=avatar_url)
        
        button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Avatar", emoji="<:download:1222150229118160976>", url=avatar_url)
        view = discord.ui.View()
        view.add_item(button)
        
        await ctx.reply(embed=embed, view=view, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="banner", description="Get the user banner of any user")
    async def banner(self, ctx, user: discord.User = None):
        user = user or ctx.author

        try:
            fetched_user = await self.client.fetch_user(user.id)

            banner_url = str(fetched_user.banner) if fetched_user.banner else None
            embed = discord.Embed(title=f":checkered_flag: {user.display_name}'s Banner", color=0xB19D30)

            if banner_url:
                embed.set_image(url=banner_url)

                button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Banner", emoji="<:download:1222150229118160976>", url=banner_url)
                view = discord.ui.View()
                view.add_item(button)

                await ctx.reply(embed=embed, view=view, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            else:
                embed.description = f"Whoops! {user.display_name} has no profile banner."
                await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        
        except discord.NotFound:
            await ctx.reply("User not found., mention_author=False, allowed_mentions=discord.AllowedMentions.none()")
        except discord.HTTPException as e:
            await ctx.reply(f"An error occurred while processing your request: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except Exception as e:
            await ctx.reply(f"An unexpected error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="botinfo", description="Get information about the bot", aliases=["binfo", "info"])
    async def botinfo(self, ctx):
        created_at_timestamp = int(self.client.user.created_at.timestamp())
        created_at = f"<t:{created_at_timestamp}:D>"
        server_count = len(self.client.guilds)
        total_users = sum(guild.member_count for guild in self.client.guilds)

        embed = discord.Embed(
            title="✨ About Strexify",
            color=0xB19D30
        )

        embed.add_field(name="\u2001", value="\u2001", inline=False)

        embed.add_field(name=":alarm_clock: Bot Created", value=f"• {created_at}", inline=False)
        embed.add_field(name=":link: Website", value=f"• [**strexify.xyz**](https://strexify.xyz)", inline=False)
        embed.add_field(name=":computer: Host", value="• [**Cybrancee**](https://cybrancee.com)", inline=False)
        embed.add_field(name=":bar_chart: Working for", value=f"• **{server_count} servers**\n• **{total_users} users**", inline=False)

        embed.add_field(name=":symbols: Prefixes", value="`=` or `/`", inline=False)
        embed.add_field(name=":newspaper: Developer", value="• [**Strexx**](https://discordapp.com/users/602092087957127179)", inline=False)

        embed.add_field(name=":people_hugging: With the Help of", value=(
            "• [**Kiki124**](https://discordapp.com/users/1105414178937774150)\n"
            "• [**Franki1902**](https://discordapp.com/users/833752068300210236)\n"
            "• [**LS_Wartaal**](https://discordapp.com/users/817767356973580298)\n"
            "• [**XTHESilent**](https://discordapp.com/users/1178657876823265320)\n"
            "• [**Phantom.py**](https://discordapp.com/users/1178278763180609587)"
        ), inline=False)

        button_website = discord.ui.Button(style=discord.ButtonStyle.link, label="Website", emoji="<:NE_Web:1089813122111520842>", url="https://strexify.xyz")
        button_tos = discord.ui.Button(style=discord.ButtonStyle.link, label="TOS", emoji="<a:amonkaTOS:597590453180825600>", url="https://strexify.xyz/terms")

        view = discord.ui.View()
        view.add_item(button_website)
        view.add_item(button_tos)

        embed.set_thumbnail(url=self.client.user.avatar.url)

        embed.set_footer(text="Use /help for a list of commands.", icon_url="https://cdn.discordapp.com/attachments/1169358000960589929/1196935506823495881/1869px-Python-logo-notext.png?ex=65b9700e&is=65a6fb0e&hm=3372bc72db3f2f40cd67f6362544d426ec6734d07d9f6043f4c917a411eef796&size=20")

        await ctx.reply(embed=embed, view=view, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="developer", description="Get the bot developer's Discord", aliases=["dev"])
    async def developer(self, ctx):
        developer_id = 602092087957127179
        developer = await self.client.fetch_user(developer_id)

        embed = discord.Embed(
            title="Strexify's Developer",
            description="I was programmed by [**Strexx!**](https://discord.com/users/602092087957127179)\nFeel free to DM him for any questions!",
            color=0xB19D30
        )

        embed.set_thumbnail(url=developer.avatar.url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="help", description="Get a list of the bot's commands")
    async def help(self, ctx, *, command_name: str = None):
        try:
            bot_avatar_url = self.client.user.avatar.url if self.client.user.avatar else discord.Embed.Empty

            embed = discord.Embed(title="📜 Bot Commands", color=0xB19D30)
            embed.set_thumbnail(url=bot_avatar_url)

            if command_name:
                command = discord.utils.get(self.client.commands, name=command_name.lower())
                if command:
                    embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/6564-activedev-yellow.png")
                    embed.add_field(name=f"Command: `/{command.name}`", value=command.description, inline=False)
                else:
                    embed.add_field(name="😢 Whoops!", value=f"Command `/{command_name}` not found.", inline=False)
                
                await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            else:
                all_commands = {cmd.name: cmd for cmd in self.client.commands}
                for cog in self.client.cogs.values():
                    for cmd in cog.get_commands():
                        all_commands[cmd.name] = cmd

                all_commands = sorted(all_commands.values(), key=lambda x: x.name)
                command_names = [f"• {command.name}" for command in all_commands]

                pages = [command_names[i:i + 25] for i in range(0, len(command_names), 25)]
                total_pages = len(pages)

                current_page = 0

                def update_embed():
                    embed.clear_fields()
                    embed.add_field(name=f"List of commands [Page {current_page + 1}/{total_pages}]", value="\n".join(pages[current_page]), inline=False)
                    embed.add_field(name="Additional Information", value="Dm **@strexy.** for more info!", inline=False)
                    return embed

                msg = await ctx.reply(embed=update_embed(), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
                await msg.add_reaction("⬅️")
                await msg.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == msg.id

                while True:
                    try:
                        reaction, _ = await self.client.wait_for("reaction_add", check=check)

                        if str(reaction.emoji) == "⬅️":
                            current_page = (current_page - 1) % total_pages
                        elif str(reaction.emoji) == "➡️":
                            current_page = (current_page + 1) % total_pages

                        await msg.edit(embed=update_embed())
                        await msg.remove_reaction(reaction, ctx.author)
                    except discord.errors.NotFound:
                        break

                await msg.clear_reactions()

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="host", description="Get the bot's hosting website")
    async def host(self, ctx):
        image_url = "https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_87ceb358523ce762ba40369c18687800/cybrancee.png"

        embed = discord.Embed(
            title="Hosting Website",
            description="I am currently being hosted in [**Cybrancee!**](https://cybrancee.com)",
            color=0xB19D30
        )

        embed.set_thumbnail(url=image_url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="invite", description="Add the bot to your own server", aliases=["inv", "invitelink", "addbot"])
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite Strexify to your Discord server!",
            description="Click the link below to add Strexify to your server.",
            color=0xB19D30
        )
        embed.add_field(name="Invite Link", value="[**Invite me now!**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)")

        embed.set_thumbnail(url="https://simtric.net/soft/Links/icon.png")

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="joindate", description="Check the server join date for any user")
    async def joindate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        join_date = member.joined_at.timestamp()

        embed = discord.Embed(
            title=f"{member.display_name} joined the server",
            color=0xB19D30,
            description=f"{member.mention} has joined the server <t:{int(join_date)}:R>!",
        )

        embed.set_thumbnail(url=member.avatar.url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="ping", description="Check the bot's latency", aliases=["ms", "latency"])
    async def ping(self, ctx):
        try:
            start_time = time.time()
            await asyncio.sleep(0.5)
            end_time = time.time()
            server_latency = round((end_time - start_time) * 1000)

            api_latency = round(ctx.bot.latency * 1000)

            embed = discord.Embed(
                title="<:website:1222517584369549425> Pong!",
                description=f"You were too slow!\n- **API Latency:** `{api_latency}`\n- **Server Latency:** `{server_latency}`",
                color=0xB19D30
            )
            embed.set_thumbnail(url="https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/1f3d3.png")
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="roles", description="Check any user's roles")
    async def roles(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        sorted_roles = sorted(member.roles[1:], key=lambda role: role.position, reverse=True)

        roles_mentions = [f"• <@&{role.id}>" for role in sorted_roles]

        embed = discord.Embed(
            title=f"{member.display_name}'s Roles",
            color=0xB19D30,
            description="\n".join(roles_mentions) if roles_mentions else "No roles",
        )

        embed.set_thumbnail(url=member.avatar.url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="servercount", description="Shows the number of servers the bot is in")
    async def servercount(self, ctx):
        server_count = len(self.client.guilds)

        embed = discord.Embed(
            title=":rotating_light: Server Count",
            description=f"The bot is currently in **{server_count} servers!**\n• [**Invite me to your server! :link:**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)",
            color=0xB19D30
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/541/541555.png")

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="serverinfo", description="Get info about the server")
    async def serverinfo(self, ctx):
        server = ctx.guild
        embed = discord.Embed(title=f"{server.name}", color=0xB19D30)

        if server.icon:
            embed.set_thumbnail(url=str(server.icon.url))
        
        operators = sum(1 for member in server.members if member.guild_permissions.administrator and not member.bot)
        newest_member = max(server.members, key=lambda m: m.joined_at)

        description = (
            f"- :crown: Owner: {server.owner.mention}\n"
            f"- :busts_in_silhouette: Members: {server.member_count}\n"
            f"- :gem: Boosts: {server.premium_subscription_count}\n"
            f"- :medal: Roles: {len(server.roles)}\n"
            f"- :calendar: Created: <t:{int(server.created_at.timestamp())}:F>\n"
            f"- :crown: Administrators: {operators}\n"
            f"- :wave: Newest Member: {newest_member.mention if not newest_member.bot else 'Not available'}"
        )


        embed.description = description

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="team", description="Display a list of the bot's team")
    async def team(self, ctx):
        try:
            guild_id = 1185320952448430180
            guild = self.client.get_guild(guild_id)

            role_ids = [
                1185330777311948840,
                1215632577709473822,
                1214216368241643541,
                1185331921547432076,
                1185331791301705758,
                1201981013144916088,
                1185332186774245456,
                1201980813345038438,
                1185332267606888569,
                1206253546933329930,
            ]

            team_members = [
                member
                for member in guild.members
                if any(role.id in role_ids for role in member.roles)
            ]

            team_members.sort(key=lambda x: max(x.roles, key=lambda r: r.position).position)

            members_list = "\n".join(
                [f"• {member.display_name}" for member in team_members]
            )

            embed = discord.Embed(
                title="🤖 Team Members",
                description=f"**Here's a list of the bot's team:**\n\n{members_list}",
                color=0xB19D30,
            )

            embed.set_thumbnail(
                url="https://www.iconpacks.net/icons/1/free-network-team-icon-308-thumb.png"
            )

            await ctx.reply(
                embed=embed,
                mention_author=False,
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except Exception as e:
            await ctx.reply(
                f"An error occurred: {e}",
                mention_author=False,
                allowed_mentions=discord.AllowedMentions.none(),
            )

    @commands.hybrid_command(name="test", description="Test if the bot is running")
    async def test(self, ctx):
        await ctx.reply("Yep, I'm working fine!", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="timestamp", description="Get a timestamp for any specific date")
    async def timestamp(self, ctx, yyyy: int = None, mm: int = None, dd: int = None, hh: int = None, min: int = None):
        try:
            if yyyy is None or mm is None or dd is None or hh is None or min is None:
                specified_datetime = datetime.datetime.now()
            else:
                specified_datetime = datetime.datetime(yyyy, mm, dd, hh, min)

            formatted_timestamps = [
                f"<t:{int(specified_datetime.timestamp())}:f> **//** `<t:{int(specified_datetime.timestamp())}:f>`",
                f"<t:{int(specified_datetime.timestamp())}:T> **//** `<t:{int(specified_datetime.timestamp())}:T>`",
                f"<t:{int(specified_datetime.timestamp())}:t> **//** `<t:{int(specified_datetime.timestamp())}:t>`",
                f"<t:{int(specified_datetime.timestamp())}:D> **//** `<t:{int(specified_datetime.timestamp())}:D>`",
                f"<t:{int(specified_datetime.timestamp())}:d> **//** `<t:{int(specified_datetime.timestamp())}:d>`",
                f"<t:{int(specified_datetime.timestamp())}:F> **//** `<t:{int(specified_datetime.timestamp())}:F>`",
                f"<t:{int(specified_datetime.timestamp())}:R> **//** `<t:{int(specified_datetime.timestamp())}:R>`"
            ]

            timestamp_types = [
                "Full Date",
                "Long Time",
                "Short Time",
                "Long Date",
                "Short Date",
                "Full Date",
                "Relative Time"
            ]

            embed = discord.Embed(title="⏰ Timestamps", color=0xB19D30)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1674/1674929.png")

            for timestamp_type, timestamp_value in zip(timestamp_types, formatted_timestamps):
                embed.add_field(name=timestamp_type, value=timestamp_value, inline=False)

            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

            await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        except ValueError as e:
            await ctx.reply(f"**Invalid date or time values.** {e}\nPlease use the following format: ```/timestamp YYYY MM DD HH MM```", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="uptime", description="Check how long the bot has been online for")
    async def uptime(self, ctx):
        uptime_delta = datetime.datetime.utcnow() - self.client.startTime
        uptime_timestamp = int((datetime.datetime.utcnow() - uptime_delta).timestamp())
        uptime_str = f"<t:{uptime_timestamp}:R>"

        embed = discord.Embed(
            title="Bot Uptime",
            description=f"Strexify has been running since {uptime_str}.",
            color=0xB19D30
        )

        embed.set_thumbnail(url=self.client.user.avatar.url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="usercount", description="Shows the total number of users the bot can see")
    async def usercount(self, ctx):
        try:
            total_users = sum(guild.member_count for guild in self.client.guilds)

            embed = discord.Embed(
                title=":busts_in_silhouette: User Count",
                description=f"The bot can see a total of **{total_users} users!**\n• [**Invite me to your server! :link:**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)",
                color=0xB19D30
            )
            embed.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/56880/busts-in-silhouette-emoji-clipart-xl.png")

            await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except discord.HTTPException as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())


    @commands.hybrid_command(name="userinfo", description="Get info about any user")
    async def userinfo(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author

        nickname = user.nick if user.nick else "None"
        is_bot = "True" if user.bot else "False"
        created_at_timestamp = f"<t:{int(user.created_at.timestamp())}:F>"
        join_date_timestamp = f"<t:{int(user.joined_at.timestamp())}:F>"
        highest_role = user.top_role.mention if user.top_role.name != "@everyone" else "No roles"
        full_perms = "True" if user.guild_permissions.administrator else "False"
        is_boosting = "True" if user.premium_since else "False"

        embed = discord.Embed(
            title=f"{user.display_name}'s User Information",
            description=(
                f"- :bust_in_silhouette: User: {user.mention}\n"
                f"- :identification_card: Username: {user.name}\n"
                f"- :identification_card: User ID: `{user.id}`\n"
                f"- :name_badge: Nickname: {nickname}\n"
                f"- :robot: Bot: {is_bot}\n"
                f"- :calendar: Created at: {created_at_timestamp}\n"
                f"- :calendar: Joined at: {join_date_timestamp}\n"
                f"- :medal: Highest Role: {highest_role}\n"
                f"- :crown: Full Perms: {full_perms}\n"
                f"- :gem: Boosting: {is_boosting}"
            ),
            color=0xB19D30,
        )

        embed.set_thumbnail(url=user.avatar.url)

        button_userinfo = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Avatar", emoji="<:download:1222150229118160976>", url=user.avatar.url)
        button_roles = discord.ui.Button(style=discord.ButtonStyle.red, label="View Roles", emoji="<a:bluecrown:1222150961859133460>")

        async def roles_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Here are the roles of the user:", ephemeral=True, embed=await self.generate_roles_embed(interaction.user, user))

        button_roles.callback = roles_callback

        view = discord.ui.View()
        view.add_item(button_userinfo)
        view.add_item(button_roles)

        await ctx.reply(embed=embed, view=view, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    async def generate_roles_embed(viewer: discord.Member, user: discord.Member) -> discord.Embed:
        sorted_roles = sorted(user.roles[1:], key=lambda role: role.position, reverse=True)
        roles_mentions = [f"• <@&{role.id}>" for role in sorted_roles]
        
        embed = discord.Embed(
            title=f"{user.display_name}'s Roles",
            color=0xB19D30,
            description="\n".join(roles_mentions) if roles_mentions else "No roles",
        ) 
        
        embed.set_thumbnail(url=user.avatar.url)
        
        return embed


    @commands.hybrid_command(name="weather", description="Check the weather in any city")
    async def weather(self, ctx, city):

        api_key = '5df942193c75eba20ccbc35c4a539b4b'

        base_url = 'http://api.weatherstack.com/current'

        params = {'access_key': api_key, 'query': city}


        try:
            response = requests.get(base_url, params=params)

            response.raise_for_status()  
            
            data = response.json()
            temperature = data['current']['temperature']
            weather_description = data['current']['weather_descriptions'][0]
            observation_time = data['current']['observation_time']

            embed = discord.Embed(title=f':white_sun_rain_cloud: Weather in {city.capitalize()}', color=0xB19D30)

            embed.add_field(name='🔥 Temperature', value=f'{temperature}°C', inline=False)
            embed.add_field(name=':white_sun_rain_cloud: Weather', value=weather_description, inline=False)
            embed.add_field(name='⌚ Local Time', value=observation_time, inline=False)

            embed.set_thumbnail(url="https://icons.iconarchive.com/icons/alecive/flatwoken/512/Apps-Weather-icon.png")

            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

            await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        except requests.exceptions.RequestException as e:
            await ctx.reply(f"Error fetching weather data: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())


async def setup(client):
  await client.add_cog(Info(client))