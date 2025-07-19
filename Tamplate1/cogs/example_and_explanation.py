# cog 예시본입니다.
# cog를 사용하는 이유는 봇을 중지하지 않고 코드를 수정하고 기능을 추가 / 제거하는 등의 작업이 가능하기 때문입니다.
# 봇을 중지하지 않으면 큰 장점들이 많은데 대표적으로 ui.View(ui.button, ui.select 등등)가 다른 cog에 있을 경우 View가 유지되기 때문입니다.
# 여러 서버에서 봇을 사용하는 경우 봇이 일일히 서버에 View를 다시 전송할 필요가 없어지는거죠.
# 단 이 코드에서 사용하는 버튼 방식은 리로드시 로직이 업데이트 되지 않습니다.
# 쉽게 말 해서 버튼1을 눌렀을 때 asdf를 전송하게 했다가 zxcv를 보내도록 수정을 한 뒤 봇을 재시작 해도 코드를 수정하기 전에 전송된 버튼에서는 여전히 asdf를 보낸다는거죠.
# 코드 업데이트 시 수정된 코드가 반영되는 버튼은 아직 다 만들지 못해서 조만간 가져오겠습니다 :)

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

    # 이 함수는 main() 함수입니다. 봇 코드에 보면 메인 !start 명령을 이용해 각 cog의 main() 함수를 실행시키는걸 볼 수 있습니다.
    # 이렇게 만든 이유는 간단합니다. !start를 이용해 이 cog를 포함한 모든 cog의 main()을 실행할 수 있지만 !send_button을 이용해 이 cog의 main() 함수만 실행시키는것도 가능하기 때문입니다.
    # 여기서 권장되는것은 다른 cog와 커멘드의 이름이 겹치지 않도록 커멘드 앞에 이 cog를 의미하는 문자를 붙이는겁니다. 이 버튼은 example의 앞글자인 ex를 따와서 ex_send_button이 되었죠.
    @commands.command(name="ex_sned_button")
    async def main(self, ctx):
        await ctx.send("button!", view=TestButton(self.bot))

# 이 함수는 cog 사용에 반드시 필요한 함수입니다. 어떤 cog든 이 setup() 함수가 빠지면 안됩니다.
async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot)) # bot.add_cog()는 commands.Cog로 만들어진 클래스를 인수로 받습니다. 이 함수를 이용해야 클래스가 봇에서 사용 가능하게 됩니다.
    print(f"Cog {__name__} is now available.")
