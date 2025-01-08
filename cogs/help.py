import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """顯示所有 Cog 的指令及說明"""
        # 建立下拉選單的選項，這裡會列出所有 Cog 名稱
        options = [
            discord.SelectOption(label="!memo", description="新增備忘錄"),
            discord.SelectOption(label="!vote", description="投票"),
            discord.SelectOption(label="!roll", description="擲骰子"),
            discord.SelectOption(label="!steam", description="查Steam遊戲價格")
        ]
        
        # 創建選單
        select_menu = Select(
            placeholder="選擇一個指令查看詳細資訊",
            options=options
        )

        # 設置選擇後的回調函數
        async def select_callback(interaction: discord.Interaction):
            selected_option = select_menu.values[0]  # 用戶選擇的指令

            if selected_option == "!memo":
                usage_message = "使用方式：\n[!memo]\n"
            elif selected_option == "!vote":
                usage_message = "使用方式：\n[!vote 投票選項1 投票選項2 ... 投票選項n]\n"
            elif selected_option == "!roll":
                usage_message = (
                    "使用方式：\n[!roll 骰子數量D骰子點數]\n"
                    "範例：\n"
                    "[!roll 1D10] - 一顆10面骰子\n"
                    "[!roll 2D10] - 兩顆10面骰子"
                )
            elif selected_option == "!steam":
                usage_message = (
                    "使用方式：\n[!steam 遊戲名稱]\n"
                    "注意：\n"
                    "目前只接受英文"
                )
            # 發送使用方式訊息
            await interaction.response.send_message(usage_message, ephemeral=True)

        select_menu.callback = select_callback

        # 創建 View 並將選單添加進去
        view = View()
        view.add_item(select_menu)

        # 發送訊息，顯示下拉選單
        await ctx.send("請選擇一個指令查看其詳細資訊：", view=view)

# 註冊 Cog
def setup(bot):
    bot.add_cog(HelpCog(bot))
