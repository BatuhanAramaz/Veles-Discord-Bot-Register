import discord
from discord.ext import commands

class Blacklist(commands.Cog):
    def __init__(self, bot, db, config):
        self.bot = bot
        self.db = db
        self.config = config
    @commands.command()
    async def blacklist(self, ctx: commands.Context, member: discord.Member, *, reason: str):
        if not any(role.id in [int(role_id) for role_id in self.config['blacklistPermissions']] for role in ctx.author.roles):
            await ctx.send("Bu komutu kullanma yetkiniz yok.")
            return
        if self.db.is_blacklisted(str(member.id)):
            await ctx.send(f"{member.mention} zaten kara listede.")
            return
        self.db.add_to_blacklist(str(member.id), reason, str(ctx.author.id))
        blacklisted_role = ctx.guild.get_role(int(self.config['blacklistedRole']))
        if blacklisted_role:
            await member.add_roles(blacklisted_role)
            roles_to_remove = [role for role in member.roles if role.id != ctx.guild.id and role != blacklisted_role]
            await member.remove_roles(*roles_to_remove)
        embed = discord.Embed(
            title="Üye Kara Listeye Eklendi",
            description=f"{member.mention} kara listeye eklendi.",
            color=discord.Color.red()
        )
        embed.add_field(name="Sebep", value=reason)
        embed.add_field(name="Ekleyen", value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command()
    async def unblacklist(self, ctx: commands.Context, member: discord.Member):
        if not any(role.id in [int(role_id) for role_id in self.config['blacklistPermissions']] for role in ctx.author.roles):
            await ctx.send("Bu komutu kullanma yetkiniz yok.")
            return
        if not self.db.is_blacklisted(str(member.id)):
            await ctx.send(f"{member.mention} kara listede değil.")
            return
        self.db.remove_from_blacklist(str(member.id))
        blacklisted_role = ctx.guild.get_role(int(self.config['blacklistedRole']))
        if blacklisted_role and blacklisted_role in member.roles:
            await member.remove_roles(blacklisted_role)
        embed = discord.Embed(
            title="Üye Kara Listeden Çıkarıldı",
            description=f"{member.mention} kara listeden çıkarıldı.",
            color=discord.Color.green()
        )
        embed.add_field(name="Çıkaran", value=ctx.author.mention)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Blacklist(bot, bot.db, bot.config))