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


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.hybrid_command(name="ask", description="Ask the magic eightball a question", aliases=["8ball", "magiceightball" "eightball", "eight ball", "8 ball"])
    async def ask(self, ctx, *, question):
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
        await ctx.reply(response, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="coinflip", description="Flip a coin to get heads or tails", aliases=["cf", "coin", "flip", "flipcoin"])
    async def coinflip(self, ctx):
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

        message = await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        await message.add_reaction("🔄")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

        while True:
            try:
                reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
                await message.remove_reaction(reaction, ctx.author)

                value = random.randint(x, y)
                embed.description = "You got **Heads!** 👨" if value == 1 else "You got **Tails!** 🐍"

                await message.edit(embed=embed)

            except TimeoutError:
                break

    @commands.hybrid_command(name="giveaway", description="Start a first-to-react giveaway")
    async def giveaway(self, ctx, *, prize: str):
        embed = discord.Embed(
            title=":tada: GIVEAWAY :tada:",
            description=f"First to react wins:\n- {prize}\n\nHosted by: {ctx.author}",
            color=0xB19D30
        )

        contest_message = await ctx.send(embed=embed)
        await contest_message.add_reaction("\U0001F389")

        def check(reaction, user):
            return user != self.client.user and str(reaction.emoji) == "\U0001F389"
        
        embed.set_footer(text="React with :tada:")
        embed.set_thumbnail(url="https://images.emojiterra.com/google/android-12l/512px/1f381.png")

        try:
            reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=3600.0)
            congrats_embed = discord.Embed(
                title=":tada: CONGRATS :tada:",
                description=f"Congrats {user.mention}!\nYou reacted first and won {prize}",
                color=0xB19D30
            )
            congrats_message = await ctx.send(embed=congrats_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title=":tada: EXPIRED :tada:",
                description="The contest has ended.\nNo one reacted in time.",
                color=0xB19D30
            )
            timeout_embed.set_thumbnail(url="https://images.emojiterra.com/google/android-12l/512px/1f381.png")
            await ctx.send(embed=timeout_embed)

    @commands.hybrid_command(name="hug", description="Give a warm hug to another user")
    async def hug(self, ctx, user: discord.Member):
        hug_image_url = "https://cdn-icons-png.flaticon.com/512/11312/11312979.png"

        hug_embed = discord.Embed(
            title="💖 Aww!",
            color=0xB19D30,
            description=f"🤗 {ctx.author.mention} gave {user.mention} a warm hug!"
        )
        hug_embed.set_thumbnail(url=hug_image_url)

        await ctx.reply(embed=hug_embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="kindness", description="Send a kindness reminder")
    async def kindness(self, ctx):
        await ctx.reply("Hey, it's important to be nice and spread positivity. Stay happy! :smile_cat:", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="poll", description="Start a yes or no poll")
    async def poll(self, ctx, *, question: str):
        poll_embed = discord.Embed(
            title=f"\U0001F4CA Poll: {question}",
            color=0xB19D30
        )
        poll_embed.set_footer(text=f"Poll started by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        poll_message = await ctx.send(embed=poll_embed)

        await poll_message.add_reaction("<:greencheck:1209602728855085146>")
        await poll_message.add_reaction("<:redcross:1209602727328612532>")

    @commands.hybrid_command(name="roll", description="Roll a number up to 100 against the bot and see who wins")
    async def roll(self, ctx):
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

        message = await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        
        await message.add_reaction("🔄")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

        while True:
            try:
                reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
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

    @commands.hybrid_command(name="rps", description="Play rock-paper-scissors against the bot")
    async def rps(self, ctx):
        choices = ["Rock", "Paper", "Scissors"]

        def get_choice_emoji(choice):
            if choice == "Rock":
                return "<:rock_s:1222271282935107634>"
            elif choice == "Paper":
                return "<:paper_s:1222271286818902046>"
            elif choice == "Scissors":
                return "<:scissors_s:1222271285053100032>"
            else:
                return ""

        def get_bot_choice():
            return random.randint(0, 2)

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

        embed = discord.Embed(
            title="Rock Paper Scissors",
            description="React to play!",
            color=0xB19D30
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1169367882761773176/1197536486170574849/9cNwodvX0p85btOd4Zayomlo1wByYpS2D8TqALtxWYN_2j6yal11VV4MF-I8_hSTOnc.png")

        message = await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

        reactions = ["<:rock_s:1222271282935107634>", "<:paper_s:1222271286818902046>", "<:scissors_s:1222271285053100032>"]
        for reaction in reactions:
            await message.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == message.id

        try:
            while True:
                reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
                await message.remove_reaction(reaction, ctx.author)

                user_choice = reactions.index(str(reaction.emoji))
                bot_choice = get_bot_choice()

                result = determine_winner(user_choice, bot_choice)

                embed.clear_fields()
                embed.add_field(name="Your Choice", value=f"**{choices[user_choice]}** {str(reaction.emoji)}", inline=True)
                embed.add_field(name="My Choice", value=f"**{choices[bot_choice]}** {get_choice_emoji(choices[bot_choice])}", inline=True)
                embed.add_field(name="Result", value=result, inline=False)

                await message.edit(embed=embed)

        except asyncio.TimeoutError:
            pass

    @commands.hybrid_command(name="say", description="Send a message using the bot")
    async def say(self, ctx, message: str, message_link: str = None):
        channel = ctx.channel

        message = message.replace("\\n", "\n")

        if message_link:
            try:
                message_id = int(message_link.split('/')[-1])
                replied_message = await channel.fetch_message(message_id)
                await replied_message.reply(message)
                await ctx.response.send_message("Message successfully sent as a reply.", ephemeral=True)
            except Exception as e:
                await ctx.response.send_message(f"Error: {e}", ephemeral=True)
        else:
            await channel.send(message)
            await ctx.response.send_message("Message successfully sent.", ephemeral=True)

    @commands.hybrid_command(name="solve", description="Ask the bot to solve math problems", aliases=["calculate"])
    async def solve(self, ctx, *, expression):
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
            
            await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        except Exception as e:
            await ctx.reply("Please only input valid numbers and mathematical symbols for this command.", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

async def setup(client):
  await client.add_cog(Fun(client))