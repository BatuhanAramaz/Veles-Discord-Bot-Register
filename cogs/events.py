import discord
from discord.ext import commands
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, bot, db, config):
        self.bot = bot
        self.db = db
        self.config = config
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.db.add_member(str(member.id), member.name, datetime.utcnow().isoformat())
        welcome_channel = self.bot.get_channel(int(self.config['welcomeChannelId']))
        if welcome_channel:
            embed = discord.Embed(
                title="Yeni Üye!",
                description=self.config['welcomeMessage'].format(user=member.mention),
                color=int(self.config['embedColor'], 16)
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await welcome_channel.send(embed=embed)
        if not self.db.is_blacklisted(str(member.id)):
            welcome_role = member.guild.get_role(int(self.config['welcomeRole']))
            if welcome_role:
                await member.add_roles(welcome_role)
        else:
            blacklisted_role = member.guild.get_role(int(self.config['blacklistedRole']))
            if blacklisted_role:
                await member.add_roles(blacklisted_role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.db.remove_member(str(member.id))
        goodbye_channel = self.bot.get_channel(int(self.config['goodbyeChannelId']))
        if goodbye_channel:
            embed = discord.Embed(
                title="Bir Üye Ayrıldı",
                description=self.config['goodbyeMessage'].format(user=member.name),
                color=int(self.config['embedColor'], 16)
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await goodbye_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.db.add_server_log('ban', str(user.id), f"{user.name} sunucudan yasaklandı.")
        log_channel = self.bot.get_channel(int(self.config['logChannelId']))
        if log_channel:
            embed = discord.Embed(
                title="Üye Yasaklandı",
                description=self.config['banMessage'].format(user=user.name),
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.db.add_server_log('unban', str(user.id), f"{user.name} sunucudaki yasağı kaldırıldı.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            self.db.update_member_nickname(str(after.id), after.nick)

async def setup(bot):
    await bot.add_cog(Events(bot, bot.db, bot.config))