from typing import List
from discord.ext import commands
import discord
from datetime import datetime

def is_authorized(member: discord.Member, required_roles: List[int]) -> bool:
    return any(role.id in required_roles for role in member.roles)

def format_timestamp(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def get_member_status(member: discord.Member) -> str:
    if member.status == discord.Status.online:
        return "Çevrimiçi"
    elif member.status == discord.Status.idle:
        return "Boşta"
    elif member.status == discord.Status.dnd:
        return "Rahatsız Etmeyin"
    else:
        return "Çevrimdışı"

async def send_log(bot: commands.Bot, config: dict, embed: discord.Embed):
    log_channel = bot.get_channel(int(config['logChannelId']))
    if log_channel:
        await log_channel.send(embed=embed)

def create_button(label: str, custom_id: str, style: discord.ButtonStyle = discord.ButtonStyle.primary) -> discord.ui.Button:
    return discord.ui.Button(style=style, label=label, custom_id=custom_id)