# cog 예시본입니다.
# cog를 사용하는 이유는 봇을 중지하지 않고 코드를 수정하고 기능을 추가 / 제거하는 등의 작업이 가능하기 때문입니다.
# 봇을 중지하지 않으면 큰 장점들이 많은데 대표적으로 ui.View(ui.button, ui.select 등등)가 다른 cog에 있을 경우 View가 유지되기 때문입니다.
# 여러 서버에서 봇을 사용하는 경우 봇이 일일히 서버에 View를 다시 전송할 필요가 없어지는거죠.
# 단 이 코드에서 사용하는 버튼 방식은 리로드시 로직이 업데이트 되지 않습니다.
# 쉽게 말 해서 버튼1을 눌렀을 때 asdf를 전송하게 했다가 zxcv를 보내도록 수정을 한 뒤 봇을 재시작 해도 코드를 수정하기 전에 전송된 버튼에서는 여전히 asdf를 보낸다는거죠.

from discord.ext import commands
from discord import ui

class TestButton(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label="test")
    async def test_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("you click button!")
    
class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sned_button")
    async def main(self, ctx):
        await ctx.send("button!", view=TestButton(self.bot))

async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
    print(f"Cog {__name__} is now available.")
