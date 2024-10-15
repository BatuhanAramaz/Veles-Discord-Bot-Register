import discord
from discord.ext import commands
import json
import asyncio
from database.db_handler import DatabaseHandler
from cogs.events import Events
from cogs.blacklist import Blacklist
from cogs.register import Register
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
db = DatabaseHandler()
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    print('------')
    await load_cogs()
async def load_cogs():
    await bot.add_cog(Events(bot, db, config))
    await bot.add_cog(Blacklist(bot, db, config))
    await bot.add_cog(Register(bot, db, config))
    print("Tüm cog'lar yüklendi.")
@bot.command()
@commands.is_owner()
async def reload(ctx, cog: str):
    try:
        await bot.reload_extension(f"cogs.{cog}")
        await ctx.send(f"`{cog}` cog'u yeniden yüklendi.")
    except Exception as e:
        await ctx.send(f"`{cog}` cog'u yeniden yüklenirken bir hata oluştu: {e}")
async def main():
    async with bot:
        await bot.start(config['token'])
if __name__ == "__main__":
    asyncio.run(main())