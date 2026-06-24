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

def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def get_guild(data, guild_id):
    gid = str(guild_id)
    if gid not in data:
        data[gid] = {}
    return data[gid]


class Application(commands.Cog):
    """Handles auto-role qualifications and requirements configuration."""

    def __init__(self, bot):
        self.bot = bot

    # Base application command group linked to the .sin tree
    @commands.group(name="application", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def application(self, ctx):
        """Configure requirements and auto-roles for applications."""
        data = get_settings()
        g = get_guild(data, ctx.guild.id)
        role_id = g.get("application_role")
        
        if role_id:
            role = ctx.guild.get_role(int(role_id))
            role_mention = role.mention if role else f"Unknown Role ID ({role_id})"
        else:
            role_mention = "**Not Set**"

        await ctx.send(
            f"📋 **Application / Auto-role Settings:**\n"
            f"• Target Role: {role_mention}\n"
            f"• Requirements: Account age 30+ days & 500+ messages.\n\n"
            f"Use `{ctx.prefix}application role set @role` to update the role."
        )

    @application.group(name="role", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def application_role(self, ctx):
        """Subgroup helper for managing roles."""
        await ctx.send(f"Usage: `{ctx.prefix}application role set @role`")

    @application_role.command(name="set")
    @commands.has_permissions(administrator=True)
    async def application_role_set(self, ctx, role: discord.Role):
        """Sets the auto-role given to members who meet requirements."""
        data = get_settings()
        g = get_guild(data, ctx.guild.id)
        g["application_role"] = str(role.id)
        save_settings(data)
        await ctx.send(f"✅ Application auto-role has been set to {role.mention}.")


async def setup(bot):
    # Fixed: Correctly registers Application class and avoids name overlap errors
    await bot.add_cog(Application(bot))
