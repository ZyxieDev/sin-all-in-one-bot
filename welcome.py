import discord
import json
import os
from discord.ext import commands

# Shared local data file configuration paths
SETTINGS_FILE = "guild_settings.json"

def get_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def get_guild(data, guild_id):
    gid = str(guild_id)
    if gid not in data:
        data[gid] = {}
    return data[gid]


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This runs automatically when a new member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        data = get_settings()
        g = get_guild(data, member.guild.id)
        channel_id = g.get("welcome_channel")
        
        if channel_id:
            channel = member.guild.get_channel(int(channel_id))
            if channel:
                embed = discord.Embed(
                    title="👋 Welcome to the Server!",
                    description=f"Welcome {member.mention}! We are so glad to have you here with us. 🎉",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass

    # This runs automatically when a member leaves the server
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        data = get_settings()
        g = get_guild(data, member.guild.id)
        channel_id = g.get("bye_channel")
        
        if channel_id:
            channel = member.guild.get_channel(int(channel_id))
            if channel:
                embed = discord.Embed(
                    title="😢 Goodbye!",
                    description=f"**{member.name}** has left the server. We will miss you! 💔",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass


async def setup(bot):
    await bot.add_cog(Welcome(bot))
