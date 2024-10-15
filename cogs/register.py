import discord
from discord.ext import commands
import asyncio
from typing import Optional

class Register(commands.Cog):
    def __init__(self, bot, db, config):
        self.bot = bot
        self.db = db
        self.config = config

    @commands.command()
    async def register(self, ctx: commands.Context, member: discord.Member, name: str, age: Optional[int] = None):
        if not any(role.id in [int(role_id) for role_id in self.config['registerPermissions']] for role in ctx.author.roles):
            await ctx.send("Bu komutu kullanma yetkiniz yok.")
            return
        if ctx.channel.id not in [int(channel_id) for channel_id in self.config['registerChannels']]:
            await ctx.send("Bu komutu yalnızca kayıt kanallarında kullanabilirsiniz.")
            return
        member_info = self.db.get_member_info(str(member.id))
        is_blacklisted = self.db.is_blacklisted(str(member.id))
        embed = discord.Embed(
            title="Üye Kayıt Bilgileri",
            color=int(self.config['embedColor'], 16)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Kullanıcı Adı", value=member.name, inline=False)
        embed.add_field(name="Daha Önce Banlandı mı?", value="Hayır" if not member_info else "Evet", inline=False)
        embed.add_field(name="Daha Önce Kicklendi mi?", value="Bilinmiyor", inline=False)
        embed.add_field(name="Kara Listede mi?", value="Evet" if is_blacklisted else "Hayır", inline=False)
        view = discord.ui.View()
        if self.config.get('registerType') == 1 and self.config.get('gender'):
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="Erkek", custom_id="register_male"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="Kadın", custom_id="register_female"))
        else:
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label="Kaydet", custom_id="register_save"))
        message = await ctx.send(embed=embed, view=view)
        def check(interaction: discord.Interaction):
            return interaction.message.id == message.id and interaction.user.id == ctx.author.id

        try:
            interaction = await self.bot.wait_for('interaction', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.edit(content="Kayıt işlemi zaman aşımına uğradı.", view=None)
            return
        role = None
        if interaction.custom_id == "register_male":
            role = ctx.guild.get_role(int(self.config['manRole']))
        elif interaction.custom_id == "register_female":
            role = ctx.guild.get_role(int(self.config['womanRole']))

        if role:
            await member.add_roles(role)
            welcome_role = ctx.guild.get_role(int(self.config['welcomeRole']))
            if welcome_role in member.roles:
                await member.remove_roles(welcome_role)
        new_nickname = f"{name} | {age}" if self.config.get('registerType') == 1 and age else name
        await member.edit(nick=new_nickname)
        self.db.update_member_nickname(str(member.id), new_nickname)
        log_channel = self.bot.get_channel(int(self.config['registerLogChannelId']))
        if log_channel:
            log_embed = discord.Embed(
                title="Üye Kaydedildi",
                color=discord.Color.green()
            )
            log_embed.add_field(name="Kaydedilen Üye", value=member.mention, inline=False)
            log_embed.add_field(name="Kaydeden Yetkili", value=ctx.author.mention, inline=False)
            log_embed.add_field(name="Verilen İsim", value=new_nickname, inline=False)
            log_embed.add_field(name="Katılma Tarihi", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            log_embed.set_thumbnail(url=member.display_avatar.url)
            await log_channel.send(embed=log_embed)

        await interaction.response.send_message(f"{member.mention} başarıyla kaydedildi!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Register(bot, bot.db, bot.config))