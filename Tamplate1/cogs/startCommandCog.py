from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def main(self, ctx):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
    print(f"Cog {__name__} is now available.")
