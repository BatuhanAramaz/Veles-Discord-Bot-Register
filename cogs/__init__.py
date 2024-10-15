from .events import Events
from .blacklist import Blacklist
from .register import Register

__all__ = ['Events', 'Blacklist', 'Register']

async def setup(bot):
    await bot.add_cog(Events(bot, bot.db, bot.config))
    await bot.add_cog(Blacklist(bot, bot.db, bot.config))
    await bot.add_cog(Register(bot, bot.db, bot.config))