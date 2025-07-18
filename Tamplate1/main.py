import discord, os, json, io
from discord.ext import commands

file_path = os.path.dirname(os.path.abspath(__file__)) # 파일 구조는 Tamplate1 내부와 같이 되있을 때를 기준으로 합니다.
use_cogs = [file.split(".")[0] for file in os.listdir(f"{file_path}/cogs") if ".py" in file] # ./cogs 내부에 있는 모든 파이썬 파일(.py)의 목록을 가져옵니다.
server_data_mod = "main" # **중요**  데이터 모드를 변경하여 사용할 수 있습니다. 전 개인적으로 main과 test를 사용합니다. main은 실전 사용에서 쓰고 test는 테스트용 서버에서 구동할 때 씁니다.
command_prefix = "!" # Context 커멘드 사용 시 사용할 접두사를 지정합니다.
TOKEN = "TOKEN" # 봇 토큰입니다. **이 방식은 권장되지 않으며 보안에 취약할 수 있습니다. env와 같은 보안을 사용할 것을 권장합니다.**
TESTTOKEN = "TOKEN" # 테스트용 봇 토큰입니다. (실제 사용할 봇 계정이 아닌 태스트용 계정을 이용할 때 편하게 하기 위해 사용)

class Bot(commands.Bot):
    async def setup_hook(self): # on_ready()와는 다르게 세션이 초기화 되도 작동하지 않습니다.
        with open(f"{file_path}/data/{server_data_mod}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data["file_path"] = file_path
        bot.bot_data = data
        for cog in use_cogs:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Cog {cog} has been loaded.')
        try:
            synced = await bot.tree.sync()
            print(f"synced {len(synced)} commands")
        except Exception as e:
            print(e)
        print(f'{bot.user.name} has connected to Discord!')

bot = Bot(command_prefix=command_prefix, intents=discord.Intents.all())

@bot.command(name="load_cog")
async def load_cog(ctx, cog_name):
    "봇을 다시 실행하지 않고 cog를 불러올 수 있습니다."
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permission.")
        return
    try:
        await bot.load_extension(f"cogs.{cog_name}")
        use_cogs.append(cog_name)
        await ctx.send(f"Cog {cog_name} has been loaded.")
    except Exception as e:
        await ctx.send(f"Failed to load {cog_name}: {e}")

@bot.command(name="reload_cog")
async def reload_cog(ctx, cog_name):
    "봇을 다시 실행하지 않고 cog를 다시 불러올 수 있습니다. (오류 해결, 기능 개선 등 파일 수정 시 사용)"
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
    "봇 실행 중 cog의 값을 가져올 수 있습니다. (디버그, 오류 원인 분석 시 사용)"
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
    "./data/{server_data_mod}.json의 값을 새로고침 합니다. (데이터 파일 수정 시 사용)"
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permissions.")
        return
    try:
        with open(f"{file_path}/data/{server_data_mod}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data["file_path"] = file_path    
        bot.bot_data = data
        await ctx.send("data has been reloaded.")
    except Exception as e:
        await ctx.send(f"Error\n```{e}```")

@bot.command(name="eval")
async def run_exec(ctx: commands.Context, code: str):
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permissions.")
        return
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

@bot.command(name="start")
async def start(ctx):
    "**중요**  각 cog의 main() 함수를 실행합니다. 클래스에 main() 함수가 없는 경우 해당 클래스는 무시됩니다."
    if ctx.author.id not in bot.bot_data["admins"]:
        await ctx.send("You don't have command permissions.")
        return
    result = []
    for name, cog in bot.cogs.items():
        if hasattr(cog, "main") and callable(getattr(cog, "main")):
            await cog.main(ctx)
            result.append(name)
    await ctx.send(f"Ran {len(result)} commands. ({', '.join(result)})"

bot.run(TOKEN)
