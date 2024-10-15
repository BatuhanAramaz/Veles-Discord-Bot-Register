import discord
from datetime import datetime

def create_welcome_embed(member: discord.Member, config: dict) -> discord.Embed:
    embed = discord.Embed(
        title="Yeni Üye!",
        description=config['welcomeMessage'].format(user=member.mention),
        color=int(config['embedColor'], 16)
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Sunucuya Katılma: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
    return embed

def create_goodbye_embed(member: discord.Member, config: dict) -> discord.Embed:
    embed = discord.Embed(
        title="Bir Üye Ayrıldı",
        description=config['goodbyeMessage'].format(user=member.name),
        color=int(config['embedColor'], 16)
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Ayrılma Zamanı: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    return embed

def create_register_embed(member: discord.Member, member_info: dict, is_blacklisted: bool, config: dict) -> discord.Embed:
    embed = discord.Embed(
        title="Üye Kayıt Bilgileri",
        color=int(config['embedColor'], 16)
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Kullanıcı Adı", value=member.name, inline=False)
    embed.add_field(name="Daha Önce Banlandı mı?", value="Evet" if member_info.get('banned') else "Hayır", inline=False)
    embed.add_field(name="Daha Önce Kicklendi mi?", value="Evet" if member_info.get('kicked') else "Hayır", inline=False)
    embed.add_field(name="Kara Listede mi?", value="Evet" if is_blacklisted else "Hayır", inline=False)
    return embed

def create_blacklist_embed(member: discord.Member, reason: str, author: discord.Member, action: str) -> discord.Embed:
    color = discord.Color.red() if action == "add" else discord.Color.green()
    title = "Üye Kara Listeye Eklendi" if action == "add" else "Üye Kara Listeden Çıkarıldı"
    
    embed = discord.Embed(
        title=title,
        description=f"{member.mention} kara listeye {'eklendi' if action == 'add' else 'çıkarıldı'}.",
        color=color
    )
    if action == "add":
        embed.add_field(name="Sebep", value=reason)
    embed.add_field(name=f"{'Ekleyen' if action == 'add' else 'Çıkaran'}", value=author.mention)
    embed.set_thumbnail(url=member.display_avatar.url)
    return embed