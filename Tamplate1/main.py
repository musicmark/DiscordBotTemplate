import discord, os, json, io
from discord.ext import commands

file_path = os.path.dirname(os.path.abspath(__file__))
use_cogs = [file.split(".")[0] for file in os.listdir(f"{file_path}/cogs") if ".py" in file]
server_data_mod = "main"

class Bot(commands.Bot):
    async def setup_hook(self):
        with open(f"{file_path}/data/{server_data_mod}.json", "r", encoding="utf-8") as f:
            bot.bot_data = json.load(f)
        for cog in use_cogs:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Cog {cog} has been loaded.')
        try:
            synced = await bot.tree.sync()
            print(f"synced {len(synced)} commands")
        except Exception as e:
            print(e)
        print(f'{bot.user.name} has connected to Discord!')

bot = Bot(command_prefix='!', intents = discord.Intents.all())

@bot.command(name="load_cog")
async def load_cog(ctx, cog_name):
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permission.")
        return
    try:
        await bot.load_extension(f"cogs.{cog_name}")
        await ctx.send(f"Cog {cog_name} has been loaded.")
    except Exception as e:
        await ctx.send(f"Failed to load {cog_name}: {e}")

@bot.command(name="reload_cog")
async def reload_cog(ctx, cog_name):
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permission.")
        return
    if f"{cog_name}.py" in use_cogs:
        try:
            await bot.reload_extension(f"cogs.{cog_name}")
            await ctx.send(f"Cog {cog_name} has been reloaded.")
        except Exception as e:
            await ctx.send(f"Failed to reload {cog_name}: {e}")
    else:
        await ctx.send(f"Cog {cog_name} is not loaded.")

@bot.command(name="get_cog_value")
async def get_cog_value(ctx, cog_name, value):
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permission.")
        return
    if f"{cog_name}.py" in use_cogs:
        cog = bot.cogs[cog_name]
        if hasattr(cog, value):
            cog_value = getattr(cog, value)
            await ctx.send(f"{value}: {cog_value}")
        else:
            await ctx.send(f"{value} not found in {cog_name}.")
    else:
        await ctx.send(f"Cog {cog_name} was not found.")

@bot.command(name="reload_data")
async def reload_data(ctx):
    try:
        with open(f"{file_path}/data/{server_data_mod}.json", "r", encoding="utf-8") as f:
            bot.bot_data = json.load(f)
        await ctx.send("data has been reloaded.")
    except Exception as e:
        await ctx.send(f"Error\n```{e}```")

@bot.command(name="eval")
async def run_exec(ctx: commands.Context, code: str):
    if ctx.author.id in bot.bot_data["admins"]:
        try:
            result = eval(code, globals())

            if len(str(result)) >= 1999:
                with io.StringIO() as f:
                    f.write(str(result))
                    f.seek(0)
                    file = discord.File(f, filename="exec_output.txt")
                    await ctx.send("Output is too long. Here is the file:", file=file)
                    return

            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error\n```{e}```")
    else:
        await ctx.send("You don't have command permissions.")

@bot.command(name="start")
async def start(ctx):
    for cog in bot.cogs.items():
        print(cog)
        await cog[1].main(ctx)

TOKEN = "TOKEN"
TESTTOKEN = "TOKEN"

bot.run(TOKEN)
