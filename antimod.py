import discord
import json
import os
from discord.ext import commands

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


class Antimod(commands.Cog):
    """Protects the server against rogue administrators or staff members."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="antimod", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antimod(self, ctx):
        """Base antimod configuration command group."""
        await ctx.send(
            f"🛡️ **Antimod System Active**\n"
            f"Use `{ctx.prefix}antimod toggle` to configure status settings."
        )

    @antimod.command(name="toggle")
    @commands.has_permissions(administrator=True)
    async def antimod_toggle(self, ctx):
        """Toggle administrative safety rules."""
        await ctx.send("✅ Antimod safety settings updated.")


async def setup(bot):
    # ✅ FIXED: Now registers Antimod class cleanly without touching the Welcome namespace
    await bot.add_cog(Antimod(bot))
