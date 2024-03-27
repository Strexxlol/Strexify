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

class Lists(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_joke.start()
        self.daily_quote.start()
              
    @tasks.loop(hours=24)
    async def daily_joke(self):
        Channel = self.client.get_channel(1203368779673903235)

        today = datetime.datetime.utcnow().date()
        async for message in Channel.history(limit=1):
            if message.created_at.date() == today:
                return

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

        random_joke = random.choice(jokes)

        embed = discord.Embed(
            title="Joke Time! 🤣",
            description=random_joke,
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.1/512px/1f923.png")
        embed.set_footer(text="Did you know that a new joke is sent here every day?")

        try:
            await Channel.send(embed=embed)
        except Exception as e:
            await Channel.send(f"An error occurred: {e}")

    @commands.command(name="joke", description="Get a random joke")
    async def joke(self, ctx):
        try:
            jokes = [
                "What do kids play when their mom is using the phone? Bored games.",
                "What do you call an ant who fights crime? A vigilANTe!",
                # Other jokes...
            ]
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

            message = await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            await message.add_reaction("🔄")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

            while True:
                try:
                    reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
                    await message.remove_reaction(reaction, ctx.author)

                    random_joke = random.choice(jokes)
                    embed.description = random_joke

                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    break

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())


    @tasks.loop(hours=24)
    async def daily_quote(self):
        Channel = self.client.get_channel(1203699162726666240)
        
        today = datetime.datetime.utcnow().date()
        async for message in Channel.history(limit=1):
            if message.created_at.date() == today:
                return

        motivational_quotes = [
            "Life is about making an impact, not making an income. - Kevin Kruse",
            # Other quotes...
        ]
        random_quote = random.choice(motivational_quotes)

        embed = discord.Embed(
            title="Motivation Time! 🧠",
            description=random_quote,
            color=0xB19D30
        )

        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Emoji_u1f4aa.svg/768px-Emoji_u1f4aa.svg.png")
        embed.set_footer(text="Did you know that a new quote is sent here every day!")

        try:
            await Channel.send(embed=embed)
        except Exception as e:
            await Channel.send(f"An error occurred: {e}")

    @commands.command(name="quote", description="Get a random motivational quote")
    async def quote(self, ctx):
        try:
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
    ];
            
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

            message = await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            await message.add_reaction("🔄")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == "🔄" and reaction.message.id == message.id

            while True:
                try:
                    reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
                    await message.remove_reaction(reaction, ctx.author)

                    random_quote = random.choice(motivational_quotes)
                    embed.description = random_quote

                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    break

        except Exception as e:
            await ctx.reply(f"An error occurred: {e}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())

async def setup(client):
  await client.add_cog(Lists(client))