# ✨ Welcome to Strexify - The Ultimate Solution!
# 💎 This repository contains the source code for Strexify!
# 🎭 Please do not use this code to copy, but instead learn!
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

tracemalloc.start()

# 📚 Setting up intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix=['='], intents=intents)
client.remove_command('help')

# 🔧 Setting up the bot's status
bot_status = cycle([
    "Your All-in-One solution 💖",
    "Strexifying {guild_count} servers 📢",
    "Get serious. Get Strexify ✨",
    "Power up with Strexify ⚡",
    "strexify.xyz 🔗"
])


# 🌐 Setting up the status cycle
@tasks.loop(seconds=5)
async def change_status():
    game_name = next(bot_status).format(guild_count=len(client.guilds))
    activity = discord.CustomActivity(name=game_name)
    await client.change_presence(activity=activity)

# 🌐 What shall happen once the bot runs?
@client.event
async def on_ready():
    print("-----------------------------------------------")
    print("Strexify has successfully connected to Discord!")
    print("-----------------------------------------------")
    client.startTime = datetime.datetime.utcnow()
    change_status.start()
    await client.tree.sync()
    await daily_joke.start()
    await daily_quote.start()

#   ---------------------
# / 🏠 Server commands /
# ---------------------
@client.hybrid_command(name="ping", description="Check the bot's latency", aliases=["ms", "latency"])
async def ping(ctx):
    try:
        latency = round(client.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"My reaction time is {latency}ms!",
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/1f3d3.png")
        embed.add_field(name="Server Latency:", value=f"{latency}ms", inline=True)
        embed.add_field(name="API Latency:", value=f"{round(ctx.bot.latency * 1000)}ms", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.hybrid_command(name="magiceightball", description="Ask the magic eightball a question", aliases=["8ball", "eightball", "eight ball", "8 ball", "ask"])
async def magic_eightball(ctx, *, question):
    responses = [
        "It is certain",
        "Without a doubt",
        "You may rely on it",
        "Yes definitely",
        "It is decidedly so",
        "As I see it, yes",
        "Most likely",
        "Yes",
        "Outlook good",
        "Signs point to yes",
        "Reply hazy try again",
        "Better not tell you now",
        "Ask again later",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "Outlook not so good",
        "My sources say no",
        "Very doubtful"
    ]

    response = random.choice(responses)
    await ctx.send(response)



@client.hybrid_command(name="clear", description="Clear a certain amount of messages", aliases=["purge", "delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, count: int, user: commands.MemberConverter = None):
    def check(message):
        return user is None or message.author == user
    
    await ctx.channel.purge(limit=count + 1, check=check)


@client.hybrid_command(name="sync", description="Sync the bot's slash commands")
async def sync(ctx):
    await client.tree.sync()
    await ctx.send("I have successfully synced all slash commands!")

@client.hybrid_command(name="avatar", description="Check any user's avatar", aliases=["icon", "pfp"])
async def avatar(ctx, member: discord.Member=None):
    member = ctx.author if not member else member
    avatar_url = member.avatar.url
    
    embed = discord.Embed(title=member.display_name + "'s avatar", color=0xB19D30)
    embed.set_image(url=avatar_url)
    
    button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Avatar", url=avatar_url)
    view = discord.ui.View()
    view.add_item(button)
    
    await ctx.send(embed=embed, view=view)

@client.hybrid_command(name="banner", description="Get the user banner of any user")
async def banner(ctx, user: discord.User = None):
    user = user or ctx.author

    try:
        fetched_user = await client.fetch_user(user.id)

        banner_url = str(fetched_user.banner) if fetched_user.banner else None
        embed = discord.Embed(title=f":checkered_flag: {user.display_name}'s Banner", color=0xB19D30)

        if banner_url:
            embed.set_image(url=banner_url)

            button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Banner", url=banner_url)
            view = discord.ui.View()
            view.add_item(button)

            await ctx.send(embed=embed, view=view)
        else:
            embed.description = f"Whoops! {user.display_name} has no profile banner."
            await ctx.send(embed=embed)
    
    except discord.NotFound:
        await ctx.send("User not found.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred while processing your request: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


@client.tree.command(name="say", description="Send a message using the bot")
async def say(interaction: discord.Interaction, message: str, channel: TextChannel = None):
    if channel is None:
        channel = interaction.channel

    await channel.send(message)
    await interaction.response.send_message(f"Message successfully sent in {channel.mention}.", ephemeral=True)

@client.hybrid_command(name="joined", description="Check the server join date for any user")
async def joined(ctx, member: discord.Member = None):
    member = member or ctx.author
    join_date = member.joined_at.timestamp()

    embed = discord.Embed(
        title=f"{member.display_name} joined the server",
        color=0xB19D30,
        description=f"{member.mention} has joined the server <t:{int(join_date)}:R>!",
    )

    embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)

@client.hybrid_command(name="roles", description="Check any user's roles")
async def roles(ctx, member: discord.Member = None):
    member = member or ctx.author

    sorted_roles = sorted(member.roles[1:], key=lambda role: role.position, reverse=True)

    roles_mentions = [f"• <@&{role.id}>" for role in sorted_roles]

    embed = discord.Embed(
        title=f"{member.display_name}'s Roles",
        color=0xB19D30,
        description="\n".join(roles_mentions) if roles_mentions else "No roles",
    )

    embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)


@client.hybrid_command(name="ban", description="Ban any user from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.display_name} has been banned. Reason: {reason}")

@client.hybrid_command(name="serverinfo", description="Get info about the server")
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title=f"{server.name}", color=0xB19D30)

    if server.icon:
        embed.set_thumbnail(url=str(server.icon.url))
    
    embed.add_field(name="Members :man:", value=server.member_count, inline=False)
    created_at_timestamp = f"<t:{int(server.created_at.timestamp())}:F>"
    embed.add_field(name="Server Created :alarm_clock:", value=created_at_timestamp, inline=False)
    embed.add_field(name="Roles :judge:", value=len(server.roles), inline=False)

    total_boosts = server.premium_subscription_count
    embed.add_field(name="Server Boosts :gem:", value=total_boosts, inline=False)

    await ctx.send(embed=embed)




@client.hybrid_command(name="reactiongiveaway", description="Start a first-to-react giveaway")
async def reactiongiveaway(ctx, *, prize: str):
    contest_message = await ctx.send(f"First to react to this message wins {prize}! React with :white_check_mark:")
    await contest_message.add_reaction("\U00002705")

    def check(reaction, user):
        return user != client.user and str(reaction.emoji) == "\U00002705"

    try:
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=3600.0)
        congrats_message = await ctx.send(f"Congrats {user.mention}! You reacted first and won {prize}.")
    except asyncio.TimeoutError:
        await ctx.send("The contest has ended. No one reacted in time.")

@client.hybrid_command(name="userinfo", description="Get info about any user")
async def userinfo(ctx, user_info: discord.Member = None):
    if not user_info:
        user_info = ctx.author

    embed = discord.Embed(
        title=f"{user_info.display_name}'s User Information",
        color=0xB19D30,
    )

    embed.add_field(name="User :man:", value=user_info.mention, inline=False)

    created_at_timestamp = f"<t:{int(user_info.created_at.timestamp())}:F>"
    embed.add_field(name="Account Created :alarm_clock:", value=created_at_timestamp, inline=False)

    join_date_timestamp = f"<t:{int(user_info.joined_at.timestamp())}:F>"
    embed.add_field(name="Joined Server :alarm_clock:", value=join_date_timestamp, inline=False)

    embed.add_field(name="User ID :identification_card:", value=user_info.id, inline=False)

    embed.add_field(name="Bot :robot:", value="Yes, this user is a bot." if user_info.bot else "No, this user is not a bot.", inline=False)

    highest_role = user_info.top_role.mention if user_info.top_role.name != "@everyone" else "No roles"
    embed.add_field(name="Highest Role :judge:", value=highest_role, inline=False)

    embed.set_thumbnail(url=user_info.avatar.url)

    button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download Avatar", url=user_info.avatar.url,)
    view = discord.ui.View()
    view.add_item(button)
    await ctx.send(embed=embed, view=view)




@client.hybrid_command(name="warn", description="Warn a user by sending them a private DM")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    warnings = load_warnings()

    user_id = str(member.id)

    if user_id not in warnings:
        warnings[user_id] = {"count": 1, "reasons": [reason]}
    else:
        warnings[user_id]["count"] += 1
        warnings[user_id]["reasons"].append(reason)

    total_warns = warnings[user_id]["count"]
    await member.send(f"You have been warned in **{ctx.guild.name}** for: {reason}. This is your **{total_warns}{'st' if total_warns == 1 else 'nd' if total_warns == 2 else 'rd' if total_warns == 3 else 'th'}** warning.")

    await ctx.send(f"I have warned {member.mention} for: {reason}\nThis is their **{total_warns}{'st' if total_warns == 1 else 'nd' if total_warns == 2 else 'rd' if total_warns == 3 else 'th'}** warning.")

    save_warnings(warnings)

@client.hybrid_command(name="warns", description="Check user's server warnings")
async def warns(ctx, member: discord.Member = None):
    if member is not None and ctx.message.mentions:
        member = ctx.message.mentions[0]

    if member is None:
        warnings_embed = discord.Embed(
            title=f"{ctx.guild}'s Warnings",
            color=0xB19D30,
            description="")

        if warnings:
            for user_id, user_warnings in warnings.items():
                total_warns = user_warnings["count"]
                member_from_warnings = ctx.guild.get_member(int(user_id))
                member_display_name = member_from_warnings.display_name if member_from_warnings else f"<@{user_id}>"
                warnings_embed.add_field(
                    name=f"{member_display_name}",
                    value=f"Total Warnings: {total_warns}",
                    inline=False
                )
        else:
            warnings_embed.description = f"{ctx.guild.name} has no warnings"

        warnings_embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=warnings_embed)

    else:
        user_id = str(member.id)
        if user_id in warnings:
            total_warns = warnings[user_id]["count"]
            reasons = warnings[user_id]["reasons"]
        else:
            total_warns = 0
            reasons = []

        embed = discord.Embed(
            title=f"{member.display_name}'s Warnings",
            color=0xB19D30,
            description=f"Total Warnings: {total_warns}",
        )

        if reasons:
            embed.add_field(
                name="Warning Reasons",
                value="\n".join(f"{i + 1}. {reason}" for i, reason in enumerate(reasons)),
                inline=False
            )

        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)




@client.hybrid_command(name="clearwarnings", description="Clear any user's server warnings")
@commands.has_permissions(kick_members=True)
async def clearwarnings(ctx, member: discord.Member):
    user_id = str(member.id)

    if user_id in warnings:
        del warnings[user_id]
        save_warnings(warnings)

        await ctx.send(f"All warnings for {member.mention} have been cleared.")
    else:
        await ctx.send(f"{member.mention} has no warnings.")



def save_warnings(warnings):
    with open("warnings.json", "w") as f:
        json.dump(warnings, f)

def load_warnings():
    try:
        with open("warnings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
@client.hybrid_command(name="help", description="Get a list of the bot's commands")
async def help(ctx, *, command_name: str = None):
    bot_avatar_url = client.user.avatar.url if client.user.avatar else discord.Embed.Empty

    embed = discord.Embed(title="📜 Bot Commands", color=0xB19D30)
    embed.set_thumbnail(url=bot_avatar_url)

    if command_name:
        command = discord.utils.get(client.commands, name=command_name.lower())
        if command:
            embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/6564-activedev-yellow.png")
            embed.add_field(name=f"Command: `/{command.name}`", value=command.description, inline=False)
        else:
            embed.add_field(name="😢 Whoops!", value=f"Command `/{command_name}` not found.", inline=False)
    else:
        commands_sorted = sorted(client.commands, key=lambda x: x.name)
        command_names = [f"• {command.name}" for command in commands_sorted]

        pages = [command_names[i:i + 25] for i in range(0, len(command_names), 25)]
        total_pages = len(pages)

        current_page = 0

        def update_embed():
            embed.clear_fields()
            embed.add_field(name=f"List of commands [Page {current_page + 1}/{total_pages}]", value="\n".join(pages[current_page]), inline=False)
            embed.add_field(name="Additional Information", value="Dm **@strexy.** for more info!", inline=False)
            return embed

        msg = await ctx.send(embed=update_embed())
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == msg.id

        while True:
            try:
                reaction, _ = await client.wait_for("reaction_add", check=check)

                if str(reaction.emoji) == "⬅️":
                    current_page = (current_page - 1) % total_pages
                elif str(reaction.emoji) == "➡️":
                    current_page = (current_page + 1) % total_pages

                await msg.edit(embed=update_embed())
                await msg.remove_reaction(reaction, ctx.author)
            except discord.errors.NotFound:
                break

        await msg.clear_reactions()

    await ctx.send(embed=embed)

@client.hybrid_command(name="rps", description="Play rock-paper-scissors against the bot")
async def rps(ctx):
    choices = ["Rock", "Paper", "Scissors"]

    def get_choice_emoji(choice):
        if choice == "Rock":
            return ":rock:"
        elif choice == "Paper":
            return ":roll_of_paper:"
        elif choice == "Scissors":
            return ":scissors:"
        else:
            return ""

    def get_bot_choice():
        return random.randint(0, 2)

    embed = discord.Embed(
        title="Rock-Paper-Scissors",
        description="React to play!",
        color=0xB19D30
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1169367882761773176/1197536486170574849/9cNwodvX0p85btOd4Zayomlo1wByYpS2D8TqALtxWYN_2j6yal11VV4MF-I8_hSTOnc.png")

    message = await ctx.send(embed=embed)

    reactions = ["🪨", "🧻", "✂"]
    for reaction in reactions:
        await message.add_reaction(reaction)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == message.id

    try:
        while True:
            reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)
            await message.remove_reaction(reaction, ctx.author)

            user_choice = reactions.index(str(reaction.emoji))
            bot_choice = get_bot_choice()

            result = determine_winner(user_choice, bot_choice)

            embed.clear_fields()
            embed.add_field(name="Your Choice", value=f"**{choices[user_choice]}** {str(reaction.emoji)}", inline=True)
            embed.add_field(name="My Choice", value=f"**{choices[bot_choice]}** {get_choice_emoji(choices[bot_choice])}", inline=True)
            embed.add_field(name="Result", value=result, inline=False)

            await message.edit(embed=embed)

    except TimeoutError:
        pass

def determine_winner(player_choice, bot_choice):
    if player_choice == bot_choice:
        return "GG's, it's a tie! :necktie:"
    elif (
        (player_choice == 0 and bot_choice == 2) or
        (player_choice == 1 and bot_choice == 0) or
        (player_choice == 2 and bot_choice == 1)
    ):
        return "GG's, you win! :index_pointing_at_the_viewer: :trophy:"
    else:
        return "GG's I win! :handshake: :trophy:"


    
@client.hybrid_command(name="uptime", description="Check how long the bot has been online for")
async def uptime(ctx):
    uptime_delta = datetime.datetime.utcnow() - client.startTime
    uptime_timestamp = int((datetime.datetime.utcnow() - uptime_delta).timestamp())
    uptime_str = f"<t:{uptime_timestamp}:R>"

    embed = discord.Embed(
        title="Bot Uptime",
        description=f"Strexify has been running since {uptime_str}.",
        color=0xB19D30
    )

    embed.set_thumbnail(url=client.user.avatar.url)

    await ctx.send(embed=embed)


@client.hybrid_command(name="roll", description="Roll a number up to 100 against the bot and see who wins")
async def roll(ctx):
    def generate_roll_results():
        user_result = random.randint(1, 100)
        bot_result = random.randint(1, 100)

        if user_result > bot_result:
            winner = "You win!"
        elif user_result < bot_result:
            winner = "I win!"
        else:
            winner = "It's a tie!"

        return user_result, bot_result, winner

    user_result, bot_result, winner = generate_roll_results()

    embed = discord.Embed(
        title=":100: Roll Results",
        color=0xB19D30
    )

    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7469/7469372.png")

    embed.add_field(name="You rolled", value=f"**{user_result}**", inline=False)
    embed.add_field(name="I rolled", value=f"**{bot_result}**", inline=False)
    embed.add_field(name="Winner", value=winner, inline=False)

    embed.set_footer(
        text="React with 🔄 to play again",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
    )

    message = await ctx.send(embed=embed)
    
    await message.add_reaction("🔄")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

    while True:
        try:
            reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)
            await message.remove_reaction(reaction, ctx.author)

            user_result, bot_result, winner = generate_roll_results()
            embed.set_field_at(0, name="You rolled", value=f"**{user_result}**", inline=False)
            embed.set_field_at(1, name="I rolled", value=f"**{bot_result}**", inline=False)
            embed.set_field_at(2, name="Winner", value=winner, inline=False)

            embed.set_footer(
                text="React with 🔄 to play again",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
            )

            await message.edit(embed=embed)

        except TimeoutError:
            break

@client.hybrid_command(name="poll", description="Start a yes or no poll")
async def poll(ctx, *, question: str):
    poll_embed = discord.Embed(
        title=f"\U0001F4CA Poll: {question}",
        color=0xB19D30
    )
    poll_embed.set_footer(text=f"Poll started by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

    poll_message = await ctx.send(embed=poll_embed)

    await poll_message.add_reaction("\u2705")
    await poll_message.add_reaction("\u274C")
    await ctx.message.delete()

@client.hybrid_command(name="kick", description="Kick any member from the server")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f'Successfully kicked {member.mention}.')
    await ctx.message.delete()

@client.hybrid_command(name="mute", description="Prevent any user from sending messages")
async def mute(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f":mute: {member.mention} has been muted.")

    else:
        await ctx.send("You do not have the required permissions to use this command.")

@client.hybrid_command(name="unmute", description="Allow any user to send messages after muting them")
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f":speech_balloon: {member.mention} has been unmuted.")
        else:
            await ctx.send(f":mute: I cannot unmute {member.mention} as he has not been muted.")

    else:
        await ctx.send("Sorry! You do not have the required permissions to use this command.")


@client.hybrid_command(name="solve", description="Ask the bot to solve math problems", aliases=["calculate"])
async def solve(ctx, *, expression):
    # Replace "x" with "*"
    expression = expression.replace('x', '*')

    try:
        result = eval(expression)
        rounded_result = round(result, 10)

        embed = discord.Embed(
            title=":100: Math Problem",
            color=0xB19D30,
            description=" ",
        )

        embed.add_field(name="Equation", value=f"{expression.replace('*', 'x')}", inline=False)
        embed.add_field(name="Answer", value=f"{rounded_result}", inline=False)
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1163220837101469726/1198649803563876543/210837.png?ex=65bfac9f&is=65ad379f&hm=43c7fe837b0c49169362d3a7412a8481bbf9a25398b67f162cb6b31bbe576f37")

        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Please only input valid numbers and mathematical symbols for this command.")


@client.hybrid_command(name="test", description="Test if the bot is running")
async def test(ctx):
    await ctx.reply("Yep, I'm working fine!")

@client.hybrid_command(aliases=["hey", "yo", "wsp", "wsg", "hii", "hi"], name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.send("Hello! How are you today?")

@client.hybrid_command(name="invite", description="Add the bot to your own server", aliases=["inv", "invitelink", "addbot"])
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Strexify to your Discord server!",
        description="Click the link below to add Strexify to your server.",
        color=0xB19D30
    )
    embed.add_field(name="Invite Link", value="[**Invite me now!**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)")

    embed.set_thumbnail(url="https://simtric.net/soft/Links/icon.png")

    await ctx.send(embed=embed)

@client.hybrid_command(name='banlist', aliases=['blist'], description='Displays the list of banned members')
async def banlist(ctx, user: discord.Member = None):
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

    await ctx.send(embed=embed)


@client.hybrid_command(name="unban", description="Unbans a user from the server (Use their user ID)")
@app_commands.describe(user_id='The user ID of the banned user')
async def unban(ctx, user_id: int):
    try:
        await ctx.guild.unban(discord.Object(id=user_id))

        await ctx.send(f'Successfully unbanned user with ID {user_id}.')

    except discord.HTTPException as e:
        await ctx.send(f'Failed to unban user with ID {user_id}. Error: {e}')
        
@client.hybrid_command(name="kindness", description="Send a kindness reminder")
async def kindness(ctx):
    await ctx.send("Hey, it's important to be nice and spread positivity; stay happy! :smile_cat:")

@client.hybrid_command(name="botinfo", description="Get information about the bot", alieses=["binfo", "info"])
async def botinfo(ctx):
    created_at_timestamp = int(client.user.created_at.timestamp())
    created_at = f"<t:{created_at_timestamp}:D>"
    server_count = len(client.guilds)
    total_users = sum(guild.member_count for guild in client.guilds)

    embed = discord.Embed(
        title="✨ About Strexify",
        color=0xB19D30
    )
    
    embed.add_field(name="\u2001", value="\u2001", inline=False)

    embed.add_field(name=":alarm_clock: Bot Created", value=f"• {created_at}", inline=False)
    embed.add_field(name=":link: Website", value=f"• [**strexify.xyz**](https://strexify.xyz)", inline=False)
    embed.add_field(name=":computer: Host", value="• [**Cybrancee**](https://cybrancee.com)", inline=False)
    embed.add_field(name=":bar_chart: Working for", value=f"• **{server_count} servers**\n• **{total_users} users**", inline=False)

    embed.add_field(
        name=":symbols: Prefixes",
        value="`=` or `/`",
        inline=False
    )

    embed.add_field(name=":newspaper: Developer", value="• [**Strexx**](https://discordapp.com/users/602092087957127179)", inline=False)

    embed.add_field(
        name=":people_hugging: With the Help of",
        value=(
            "• [**Kiki124**](https://discordapp.com/users/1105414178937774150)\n"
            "• [**Franki1902**](https://discordapp.com/users/833752068300210236)\n"
            "• [**LS_Wartaal**](https://discordapp.com/users/817767356973580298)\n"
            "• [**XTHESilent**](https://discordapp.com/users/1178657876823265320)\n"
            "• [**Phantom.py**](https://discordapp.com/users/1178278763180609587)"
        ),
        inline=False
)


    embed.set_thumbnail(url=client.user.avatar.url)

    embed.set_footer(text="Use /help for a list of commands.", icon_url="https://cdn.discordapp.com/attachments/1169358000960589929/1196935506823495881/1869px-Python-logo-notext.png?ex=65b9700e&is=65a6fb0e&hm=3372bc72db3f2f40cd67f6362544d426ec6734d07d9f6043f4c917a411eef796&size=20")

    await ctx.send(embed=embed)



@client.hybrid_command(name="vote", description="Get a vote link which promotes the bot")
async def vote(ctx):
     await ctx.send("Hey, please [**Vote for Strexify**](https://top.gg/bot/1168513500923056199/vote)! Voting helps promoting me, by displaying it to more and more people! :smile: :ticket:")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Whoopsies! `{ctx.message.content}` doesn't exist. Try using </help:1201186989861507197> to see a list of my available commands.")



class SuggestionModal(discord.ui.Modal, title="Bot Suggestion"):
    user_name = discord.ui.TextInput(label="Your Discord Username", placeholder="eg. cutepanda27", required=True, max_length=32, style=discord.TextStyle.short)
    suggestion = discord.ui.TextInput(label="Title Your Suggestion", placeholder="eg. Add a leveling system to the bot.", required=True, max_length=1000, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Detail Your Suggestion", placeholder="Provide detailed information about your suggestion.", required=True, min_length=20, style=discord.TextStyle.long)
    contact = discord.ui.TextInput(label="Can we contact you for further information?", placeholder="Yes, No.", required=True, max_length=20, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        server_id = 1185320952448430180
        thread_id = 1197529033567637514

        guild = client.get_guild(server_id)
        thread = discord.utils.get(guild.threads, id=thread_id)

        if thread:
            embed = discord.Embed(title=":bulb: New Suggestion", color=0xB19D30)
            embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
            embed.add_field(name=":newspaper2: Username", value=self.user_name.value, inline=False)
            embed.add_field(name=":identification_card: Suggestion Title", value=self.suggestion.value, inline=False)
            embed.add_field(name=":scroll: Description", value=self.description.value, inline=False)
            embed.add_field(name=":rotating_light: Receive Updates?", value=self.contact.value, inline=False)

            embed.set_thumbnail(url=interaction.user.avatar.url)

            suggestion_message = await thread.send(embed=embed)
            await suggestion_message.add_reaction('✅')
            await suggestion_message.add_reaction('❌')
            await interaction.response.send_message(f":love_letter: Thank you for submitting your suggestion! I have sent this to [**Strexify's Discord Server.**](https://discord.gg/fzkfvTytge) The bot management team will review it soon!", ephemeral=True)

            store_suggestion(interaction.user.id, self.user_name.value, self.suggestion.value, self.description.value, self.contact.value)
        else:
            await interaction.response.send_message("Sorry, I could not find the channel to send this suggestion.", ephemeral=True)

suggestions_list = []

def store_suggestion(user_id, user_name, suggestion_name, description, contact):
    suggestions_list.append({
        "user_id": user_id,
        "user_name": user_name,
        "suggestion_name": suggestion_name,
        "description": description,
        "contact": contact
    })

@client.tree.command(name="suggest", description="Suggest a feature for the bot")
async def suggestion_command(interaction: discord.Interaction):
    await interaction.response.send_modal(SuggestionModal())

jokes = [
    "What do kids play when their mom is using the phone? Bored games.",
    "What do you call an ant who fights crime? A vigilANTe!",
    "Why are snails slow? Because they’re carrying a house on their back.",
    "What’s the smartest insect? A spelling bee!",
    "What does a storm cloud wear under his raincoat? Thunderwear.",
    "What is fast, loud and crunchy? A rocket chip.",
    "How does the ocean say hi? It waves!",
    "What do you call a couple of chimpanzees sharing an Amazon account? PRIME-mates.",
    "Why did the teddy bear say no to dessert? Because she was stuffed.",
    "Why did the soccer player take so long to eat dinner? Because he thought he couldn’t use his hands.",
    "Name the kind of tree you can hold in your hand? A palm tree!",
    "What do birds give out on Halloween? Tweets.",
    "What has ears but cannot hear? A cornfield.",
    "What’s a cat’s favorite dessert? A bowl full of mice-cream.",
    "Where did the music teacher leave her keys? In the piano!",
    "What did the policeman say to his hungry stomach? “Freeze. You’re under a vest.”",
    "What did the left eye say to the right eye? Between us, something smells!",
    "What do you call a guy who’s really loud? Mike.",
    "Why do birds fly south in the winter? It’s faster than walking!",
    "What did the lava say to his girlfriend? “I lava you!”",
    "Why did the student eat his homework? Because the teacher told him it was a piece of cake.",
    "What did Yoda say when he saw himself in 4k? HDMI.",
    "Which superhero hits home runs? Batman!",
    "What’s Thanos’ favorite app on his phone? Snapchat.",
    "Sandy’s mum has four kids; North, West, East. What is the name of the fourth child? Sandy, obviously!",
    "What is a room with no walls? A mushroom.",
    "Why did the blue jay get in trouble at school? For tweeting on a test!",
    "What social events do spiders love to attend? Webbings.",
    "What did one pickle say to the other? Dill with it.",
    "What is brown, hairy and wears sunglasses? A coconut on vacation.",
    "Why is a football stadium always cold? It has lots of fans!",
    "What did one math book say to the other? “I’ve got so many problems.”",
    "What did the Dalmatian say after lunch? That hit the spot!",
    "What do you call two bananas on the floor? Slippers.",
    "Why did the chicken cross the playground? To get to the other slide.",
    "Why do ducks have feathers on their tails? To cover their butt quacks.",
    "How does a vampire start a letter? “Tomb it may concern…”",
    "A plane crashed in the jungle and every single person died. Who survived? Married couples.",
    "What kind of math do birds love? Owl-gebra!",
    "Why can’t you ever tell a joke around glass? It could crack up.",
    "What do you call a Star Wars droid that takes the long way around? R2 detour.",
    "How do you stop an astronaut’s baby from crying? You rocket.",
    "Why did the scarecrow win a Nobel prize? Because she was outstanding in her field.",
    "How do you know when a bike is thinking? You can see their wheels turning.",
    "Why was 6 afraid of 7? Because 7,8,9.",
    "What goes up and down but doesn’t move? The staircase.",
    "What kind of shoes do frogs love? Open-toad!",
    "How did the baby tell his mom he had a wet diaper? He sent her a pee-mail.",
    "What is a witch’s favorite subject in school? Spelling.",
    "What’s brown and sticky? A stick."
]

@tasks.loop(hours=24)
async def daily_joke():
    Channel = client.get_channel(1203368779673903235)

    today = datetime.datetime.utcnow().date()
    async for message in Channel.history(limit=1):
        if message.created_at.date() == today:
            return

    random_joke = random.choice(jokes)

    embed = discord.Embed(
        title="Joke Time! 🤣",
        description=random_joke,
        color=0xB19D30
    )

    embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.1/512px/1f923.png")

    embed.set_footer(text="Did you know that a new joke is sent here every day! (Or when the bot restarts)")

    try:
        await Channel.send(embed=embed)
    except Exception as e:
        await Channel.send(f"An error occurred: {e}")

@client.hybrid_command(name="joke", description="Get a random joke")
async def joke(ctx):
    try:
        random_joke = random.choice(jokes)

        embed = discord.Embed(
            title="Joke Time! :rofl:",
            description=random_joke,
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.1/512px/1f923.png")

        embed.set_footer(
        text="React with 🔄 to get another joke",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
    )

        message = await ctx.send(embed=embed)

        await message.add_reaction("🔄")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

        while True:
            try:
                reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)
                await message.remove_reaction(reaction, ctx.author)

                random_joke = random.choice(jokes)
                embed.description = random_joke

                await message.edit(embed=embed)

            except TimeoutError:
                break

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



motivational_quotes = [
    "Life is about making an impact, not making an income. - Kevin Kruse",
    "Whatever the mind of man can conceive and believe, it can achieve. – Napoleon Hill",
    "Strive not to be a success, but rather to be of value. – Albert Einstein",
    "Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference. – Robert Frost",
    "I attribute my success to this: I never gave or took any excuse. – Florence Nightingale",
    "You miss 100% of the shots you don’t take. – Wayne Gretzky",
    "I've missed more than 9000 shots in my career. I've lost almost 300 games. 26 times I've been trusted to take the game-winning shot and missed. I've failed over and over and over again in my life. And that is why I succeed. – Michael Jordan",
    "The most difficult thing is the decision to act, the rest is merely tenacity. – Amelia Earhart",
    "Every strike brings me closer to the next home run. – Babe Ruth",
    "Definiteness of purpose is the starting point of all achievement. – W. Clement Stone",
    "Life isn't about getting and having, it's about giving and being. – Kevin Kruse",
    "Life is what happens to you while you’re busy making other plans. – John Lennon",
    "We become what we think about. – Earl Nightingale",
    "Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails. Explore, Dream, Discover. – Mark Twain",
    "Life is 10% what happens to me and 90% of how I react to it. – Charles Swindoll",
    "The most common way people give up their power is by thinking they don’t have any. – Alice Walker",
    "The mind is everything. What you think you become. – Buddha",
    "The best time to plant a tree was 20 years ago. The second best time is now. – Chinese Proverb",
    "An unexamined life is not worth living. – Socrates",
    "Eighty percent of success is showing up. – Woody Allen",
    "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
    "Winning isn’t everything, but wanting to win is. – Vince Lombardi",
    "I am not a product of my circumstances. I am a product of my decisions. – Stephen Covey",
    "Every child is an artist. The problem is how to remain an artist once he grows up. – Pablo Picasso",
    "You can never cross the ocean until you have the courage to lose sight of the shore. – Christopher Columbus",
    "I’ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel. – Maya Angelou",
    "Either you run the day, or the day runs you. – Jim Rohn",
    "Whether you think you can or you think you can’t, you’re right. – Henry Ford",
    "The two most important days in your life are the day you are born and the day you find out why. – Mark Twain",
    "Whatever you can do, or dream you can, begin it. Boldness has genius, power and magic in it. – Johann Wolfgang von Goethe",
    "The best revenge is massive success. – Frank Sinatra",
    "People often say that motivation doesn’t last. Well, neither does bathing. That’s why we recommend it daily. – Zig Ziglar",
    "Life shrinks or expands in proportion to one's courage. – Anais Nin",
    "If you hear a voice within you say “you cannot paint,” then by all means paint and that voice will be silenced. – Vincent Van Gogh",
    "There is only one way to avoid criticism: do nothing, say nothing, and be nothing. – Aristotle",
    "Ask and it will be given to you; search, and you will find; knock and the door will be opened for you. – Jesus",
    "The only person you are destined to become is the person you decide to be. – Ralph Waldo Emerson",
    "Go confidently in the direction of your dreams. Live the life you have imagined. – Henry David Thoreau",
    "When I stand before God at the end of my life, I would hope that I would not have a single bit of talent left and could say, I used everything you gave me. – Erma Bombeck",
    "Few things can help an individual more than to place responsibility on him, and to let him know that you trust him. – Booker T. Washington",
    "Certain things catch your eye, but pursue only those that capture the heart. – Ancient Indian Proverb",
    "Believe you can and you’re halfway there. – Theodore Roosevelt",
    "Everything you’ve ever wanted is on the other side of fear. – George Addair",
    "We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light. – Plato",
    "Teach thy tongue to say, 'I do not know,' and thou shalt progress. – Maimonides",
    "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
    "When I was 5 years old, my mother always told me that happiness was the key to life. When I went to school, they asked me what I wanted to be when I grew up. I wrote down ‘happy’. They told me I didn’t understand the assignment, and I told them they didn’t understand life. – John Lennon",
    "Fall seven times and stand up eight. – Japanese Proverb",
    "When one door of happiness closes, another opens, but often we look so long at the closed door that we do not see the one that has been opened for us. – Helen Keller",
    "Everything has beauty, but not everyone can see. – Confucius"
]

@tasks.loop(hours=24)
async def daily_quote():
    Channel = client.get_channel(1203699162726666240)
    random_quote = random.choice(motivational_quotes)
    
    embed = discord.Embed(
            title="Motivation Time! 🧠",
            description=random_quote,
            color=0xB19D30
            )

    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Emoji_u1f4aa.svg/768px-Emoji_u1f4aa.svg.png")

    embed.set_footer(text=f"Did you know that a new quote is sent here everyday!")

    try:
        await Channel.send(embed=embed)
        

    except Exception as e:
        await Channel.send(f"An error occurred: {e}")

@client.hybrid_command(name="quote", description="Get a random motivational quote")
async def quote(ctx):
    try:
        random_quote = random.choice(motivational_quotes)

        embed = discord.Embed(
            title="Motivation Time! 🧠",
            description=random_quote,
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Emoji_u1f4aa.svg/768px-Emoji_u1f4aa.svg.png")

        embed.set_footer(
        text="React with 🔄 to get another quote",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
    )

        message = await ctx.send(embed=embed)

        await message.add_reaction("🔄")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

        while True:
            try:
                reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)
                await message.remove_reaction(reaction, ctx.author)

                random_quote = random.choice(motivational_quotes)
                embed.description = random_quote

                await message.edit(embed=embed)

            except TimeoutError:
                break

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")




class BugModal(discord.ui.Modal, title="Bug Report"):
    user_name = discord.ui.TextInput(label="Your Discord Username", placeholder="eg. cutepanda27", required=True, max_length=32, style=discord.TextStyle.short)
    bug = discord.ui.TextInput(label="Title Your Issue", placeholder="eg. Add a leveling system to the bot.", required=True, max_length=1000, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Detail Your Issue", placeholder="Provide detailed information about your issue.", required=True, min_length=20, style=discord.TextStyle.long)
    contact = discord.ui.TextInput(label="Can we contact you for further information?", placeholder="Yes, No.", required=True, max_length=3, min_length=2, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        server_id = 1185320952448430180
        thread_id = 1198374894757482516

        guild = client.get_guild(server_id)
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
            await bug_message.add_reaction('✅')
            await bug_message.add_reaction('❌')
            await interaction.response.send_message(f":love_letter: Thank you for submitting your issue! I have sent this to [**Strexify's Discord Server.**](https://discord.gg/fzkfvTytge) The bot management team will review it soon!", ephemeral=True)

            store_bug(interaction.user.id, self.user_name.value, self.bug.value, self.description.value)
        else:
            await interaction.response.send_message("Sorry, I could not find the channel to send this bug.", ephemeral=True)

bug_list = []

def store_bug(user_id, user_name, bug_name, description):
    bug_list.append({
        "user_id": user_id,
        "user_name": user_name,
        "bug_name": bug_name,
        "description": description
    })

@client.tree.command(name="bugreport", description="Report a bug")
async def bugreport(interaction: discord.Interaction):
    await interaction.response.send_modal(BugModal())

@client.hybrid_command(name="servercount", description="Shows the number of servers the bot is in")
async def servercount(ctx):
    server_count = len(client.guilds)

    embed = discord.Embed(
        title=":rotating_light: Server Count",
        description=f"The bot is currently in **{server_count} servers!**\n• [**Invite me to your server! :link:**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)",
        color=0xB19D30
    )
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/541/541555.png")

    await ctx.send(embed=embed)


@client.hybrid_command(name="hug", description="Give a warm hug to another user")
async def hug(ctx, user: discord.Member):
    hug_image_url = "https://cdn-icons-png.flaticon.com/512/11312/11312979.png"

    hug_embed = discord.Embed(
        title="💖 Aww!",
        color=0xB19D30,
        description=f"🤗 {ctx.author.mention} gave {user.mention} a warm hug!"
    )
    hug_embed.set_thumbnail(url=hug_image_url)

    await ctx.send(embed=hug_embed)

@client.hybrid_command(name="dm", description="Use the bot to send a direct message to a user")
@commands.has_permissions(manage_messages=True)
async def dm(ctx, user: discord.User, *, message: str):
    try:
        await user.send(f"### You've got mail! 📄\n\n\n- {message}\n\n💌 Sent from **{ctx.author.display_name}** at **{ctx.guild.name}**")

        await ctx.send(f"💌 I have sent the following message to {user.name}: {message}", ephemeral=True)
    except discord.Forbidden:
        await ctx.send("❗ Whoopsies! This user does not allow Direct messages.", ephemeral=True)

@client.hybrid_command(name="coinflip", description="Flip a coin to get heads or tails", aliases=["cf", "coin", "flip", "flipcoin"])
async def coinflip(ctx):
    x = 1
    y = 2
    value = random.randint(x, y)

    embed = discord.Embed(title="Coin Flip Result", color=0xB19D30)

    if value == 1:
        embed.description = "You got **Heads!** 👨"
    elif value == 2:
        embed.description = "You got **Tails!** 🐍"

    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/217/217853.png")

    embed.set_footer(
        text="React with 🔄 to play again",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty
    )

    message = await ctx.send(embed=embed)

    await message.add_reaction("🔄")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

    while True:
        try:
            reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)
            await message.remove_reaction(reaction, ctx.author)

            value = random.randint(x, y)
            embed.description = "You got **Heads!** 👨" if value == 1 else "You got **Tails!** 🐍"

            await message.edit(embed=embed)

        except TimeoutError:
            break


@client.hybrid_command(name="addrole", description="Add roles to any user")
async def add_role(ctx, member: discord.Member, role: discord.Role):
    try:
        if ctx.me.top_role > role and ctx.author.top_role > role:
            await member.add_roles(role)
            await ctx.send(f'Added `{role.name}` to `{member.display_name}`.')
        else:
            await ctx.send("You or the bot don't have sufficient permissions to add this role.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to add roles.")

@client.hybrid_command(name="removerole", description="Revoke roles from any user")
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    try:
        if ctx.me.top_role > role and ctx.author.top_role > role:
            await member.remove_roles(role)
            await ctx.send(f'Removed `{role.name}` from `{member.display_name}`.')
        else:
            await ctx.send("You or the bot don't have sufficient permissions to remove this role.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to remove roles.")

@client.hybrid_command(name="replacerole", description="Pick any user's role and replace it with a new one")
async def replacerole(ctx, member: discord.Member, old_role: discord.Role, new_role: discord.Role):
    try:
        if ctx.me.guild_permissions.manage_roles and ctx.author.guild_permissions.manage_roles:
            if old_role in member.roles:
                await member.remove_roles(old_role)
                await member.add_roles(new_role)
                await ctx.send(f'Replaced `{old_role.name}` with `{new_role.name}` for **{member.display_name}**.')
            else:
                await ctx.send(f'**{member.display_name}** does not have the `{old_role.name}` role.')
        else:
            await ctx.send("You or the bot don't have permission to manage roles.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage roles.")
        
@client.hybrid_command(name="nick", description="Change the nickname of any user")
async def change_nickname(ctx, member: discord.Member, *, nickname: str):
    try:
        if ctx.me.guild_permissions.manage_nicknames and ctx.author.guild_permissions.manage_nicknames:
            await member.edit(nick=nickname)
            await ctx.send(f'Changed nickname of `{member.display_name}` to `{nickname}`.')
        else:
            await ctx.send("You or the bot don't have permission to change nicknames.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change nicknames.")

@client.hybrid_command(name="rename", description="Rename any channel or category")
async def rename(ctx, target: discord.abc.GuildChannel, new_name: str):
    try:
        await target.edit(name=new_name)
        await ctx.send(f"Successfully renamed {target.mention} to it's new name!")
    except discord.Forbidden:
        await ctx.send("I don't have the necessary permissions to rename channels.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")

@client.hybrid_command(name="usercount", description="Shows the total number of users the bot can see")
async def usercount(ctx):
    try:
        total_users = sum(guild.member_count for guild in client.guilds)

        embed = discord.Embed(
            title=":busts_in_silhouette: User Count",
            description=f"The bot can see a total of **{total_users} users!**\n• [**Invite me to your server! :link:**](https://discord.com/oauth2/authorize?client_id=1168513500923056199&permissions=10741122166006&scope=bot+applications.commands)",
            color=0xB19D30
        )
        embed.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/56880/busts-in-silhouette-emoji-clipart-xl.png")

        await ctx.send(embed=embed)
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")


command_log = []

@client.event
async def on_command(ctx):
    command_log.append((ctx.command.name, ctx.author.name))

    if len(command_log) > 50:
        command_log.pop(0)

@client.hybrid_command(name="log", description="Get a log of the last 50 commands used")
async def log(ctx):
    try:
        embed = discord.Embed(
            title="📝 Command Log",
            color=0xB19D30,
        )

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5139/5139731.png")

        for command, user in command_log:
            embed.add_field(
                name=f"{user}", 
                value=f"`/{command}`", 
                inline=False
            )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        
@client.hybrid_command(name="resetnick", description="Reset anyone's server nickname")
async def reset_nick(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_nicknames:
        try:
            await member.edit(nick=None)
            await ctx.send(f"Nickname for {member.display_name} has been reset.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to reset the nickname.")
    else:
        await ctx.send("You don't have the necessary permissions to use this command.")


@client.hybrid_command(name="team", description="Display a list of the bot's team")
async def team(ctx):
    try:
        guild_id = 1185320952448430180
        guild = client.get_guild(guild_id)

        role_ids = [1185330777311948840, 1215632577709473822, 
                    1185562878137348106]

        team_members = [member for member in guild.members if any(role.id in role_ids for role in member.roles)]

        members_list = "\n".join([f"• {member.display_name}" for member in team_members])

        embed = discord.Embed(
            title="🤖 Team Members",
            description=f"**Here's a list of the bot's team:**\n\n{members_list}",
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1168513500923056199/7562afb18e7bfc8d1d3ef69260e6bc0e.png?size=1024")

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.hybrid_command(name="id", description="Get the ID of a user or role")
async def get_id(ctx, target: discord.User = None, role: discord.Role = None):
    try:
        if target:
            embed = discord.Embed(
                title="💳 User ID",
                description=f"**The ID of user {target.display_name} is**\n`{target.id}`",
                color=0xB19D30
            )

            embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/512/245/245266.png")

            await ctx.send(embed=embed)
        elif role:
            embed = discord.Embed(
                title="💳 Role ID",
                description=f"**The ID of role {role.name} is**\n{role.id}",
                color=0xB19D30
            )

            embed.set_thumbnail(url="https://cdn-icons-png.freepik.com/512/245/245266.png")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Please mention a user or provide a role to get the ID.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.hybrid_command(name="developer", description="Get the bot developer's Discord", aliases=["dev"])
async def developer(ctx):
    developer_id = 602092087957127179
    developer = await client.fetch_user(developer_id)

    embed = discord.Embed(
        title="Strexify's Developer",
        description=f"I was programmed by [**Strexx!**]({developer.avatar.url})\nFeel free to DM him for any questions!",
        color=0xB19D30
    )

    embed.set_thumbnail(url=developer.avatar.url)

    await ctx.send(embed=embed)

@client.hybrid_command(name="host", description="Get the bot's hosting website")
async def host(ctx):
    image_url = "https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_87ceb358523ce762ba40369c18687800/cybrancee.png"

    embed = discord.Embed(
        title="Hosting Website",
        description="I am currently being hosted in [**Cybrancee!**](https://cybrancee.com)",
        color=0xB19D30
    )

    embed.set_thumbnail(url=image_url)

    await ctx.send(embed=embed)


@client.hybrid_command(name="weather", description="Check the weather in any city")
async def weather(ctx, city):

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

        await ctx.send(embed=embed)

    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching weather data: {e}")

@client.hybrid_command(name="timestamp", description="Get a timestamp for any specific date")
async def timestamp(ctx, yyyy: int, mm: int, dd: int, hh: int, min: int):
    try:
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

        await ctx.send(embed=embed)

    except ValueError as e:
        await ctx.send(f"**Invalid date or time values.** {e}\nPlease use the following format: ```/timestamp YYYY MM DD HH MM```")

# 🔮 Running the bot
# 🎯 Replace 'BOTTOKEN' with your actual token.
client.run("BOTTOKEN")

# 🎉 And that is the end  of our code!
