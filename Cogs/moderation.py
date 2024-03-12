import discord
from discord.ext import commands
from discord import ui, app_commands
import json

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_log = []

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.command_log.append((ctx.command.name, ctx.author.name))

        if len(self.command_log) > 50:
            self.command_log.pop(0)

    @commands.hybrid_command(name="addrole", description="Add roles to any user")
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            if ctx.me.top_role > role and ctx.author.top_role > role:
                await member.add_roles(role)
                await ctx.reply(f'Added `{role.name}` to `{member.display_name}`.', allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("You or the bot don't have sufficient permissions to add this role.", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.reply("I don't have permission to add roles.", allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="removerole", description="Revoke roles from any user")
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        try:
            if ctx.me.top_role > role and ctx.author.top_role > role:
                await member.remove_roles(role)
                await ctx.reply(f'Removed `{role.name}` from `{member.display_name}`.', allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.reply("You or the bot don't have sufficient permissions to remove this role.", allowed_mentions=discord.AllowedMentions.none())
        except discord.Forbidden:
            await ctx.reply("I don't have permission to remove roles.", allowed_mentions=discord.AllowedMentions.none())

    @commands.hybrid_command(name="replacerole", description="Pick any user's role and replace it with a new one")
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

    @commands.hybrid_command(name="clear", description="Clear a certain amount of messages", aliases=["purge", "delete"])
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
            await user.send(f"### You've got mail! 📄\n\n\n- {message}\n\n💌 Sent from **{ctx.author.display_name}** at **{ctx.guild.name}**")

            await ctx.send(f"💌 I have sent the following message to {user.name}: {message}", ephemeral=True)
        except discord.Forbidden:
            await ctx.send("❗ Whoopsies! This user does not allow Direct messages.", ephemeral=True)

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

            for command, user in self.command_log:  # Changed command_log to self.command_log
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

    @commands.hybrid_command(name="nick", description="Change the nickname of any user")
    async def nick(self, ctx, member: discord.Member, *, nickname: str):
        try:
            if ctx.me.guild_permissions.manage_nicknames and ctx.author.guild_permissions.manage_nicknames:
                await member.edit(nick=nickname)
                await ctx.send(f'Changed nickname of `{member.display_name}` to `{nickname}`.')
            else:
                await ctx.send("You or the bot don't have permission to change nicknames.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to change nicknames.")

    @commands.hybrid_command(name="resetnick", description="Reset anyone's server nickname")
    async def reset_nick(self,ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_nicknames:
            try:
                await member.edit(nick=None)
                await ctx.send(f"Nickname for {member.display_name} has been reset.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to reset the nickname.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

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
