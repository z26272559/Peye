# cogs/memo.py
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import asyncio

memo_data = {}

class MemoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def memo(self, ctx):
        """主指令，顯示下拉式選單"""
        select_menu = Select(
            placeholder="選擇操作...",
            options=[
                discord.SelectOption(label="創建備忘錄", value="create", description="創建一個新的備忘錄"),
                discord.SelectOption(label="檢查所有備忘錄", value="check", description="檢視所有目前的備忘錄"),
                discord.SelectOption(label="刪除備忘錄", value="delete", description="刪除一個指定的備忘錄")
            ]
        )

        async def select_callback(interaction: discord.Interaction):
            if select_menu.values[0] == "create":
                await interaction.response.send_message("請輸入新的備忘錄名稱：", ephemeral=True)

                # 等待使用者輸入備忘錄名稱
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=30.0)
                    activity = msg.content

                    if activity in memo_data:
                        await ctx.send(f"活動 `{activity}` 已存在！")
                    else:
                        memo_data[activity] = {"join": [], "not_join": [], "consider": []}
                        await ctx.send(content=generate_memo_message(activity), view=create_buttons(activity))
                except asyncio.TimeoutError:
                    await ctx.send("建立備忘錄逾時，請重新操作。")

            elif select_menu.values[0] == "check":
                if not memo_data:
                    await interaction.response.send_message("目前沒有任何備忘錄！", ephemeral=True)
                else:
                    options = [discord.SelectOption(label=activity, value=activity) for activity in memo_data.keys()]
                    check_menu = Select(placeholder="選擇要檢查的備忘錄", options=options)

                    async def check_callback(check_interaction: discord.Interaction):
                        activity_to_check = check_menu.values[0]
                        await check_interaction.response.send_message(
                            content=generate_memo_message(activity_to_check),
                            view=create_buttons(activity_to_check)
                        )

                    check_menu.callback = check_callback
                    check_view = View()
                    check_view.add_item(check_menu)
                    await interaction.response.send_message("選擇要檢查的備忘錄：", view=check_view, ephemeral=True)

            elif select_menu.values[0] == "delete":
                if not memo_data:
                    await interaction.response.send_message("目前沒有任何備忘錄可以刪除！", ephemeral=True)
                    return

                options = [discord.SelectOption(label=activity, value=activity) for activity in memo_data.keys()]
                delete_menu = Select(placeholder="選擇要刪除的備忘錄", options=options)

                async def delete_callback(delete_interaction: discord.Interaction):
                    activity_to_delete = delete_menu.values[0]
                    del memo_data[activity_to_delete]
                    await delete_interaction.response.send_message(f"已刪除備忘錄 `{activity_to_delete}`")

                delete_menu.callback = delete_callback
                delete_view = View()
                delete_view.add_item(delete_menu)
                await interaction.response.send_message("選擇要刪除的備忘錄：", view=delete_view, ephemeral=True)

        select_menu.callback = select_callback
        view = View()
        view.add_item(select_menu)
        await ctx.send("選擇要執行的操作：", view=view)

def generate_memo_message(activity: str) -> str:
    """產生活動訊息"""
    join_list = memo_data[activity]["join"]
    not_join_list = memo_data[activity]["not_join"]
    consider_list = memo_data[activity]["consider"]

    join_str = "、".join(join_list) if join_list else "無"
    not_join_str = "、".join(not_join_list) if not_join_list else "無"
    consider_str = "、".join(consider_list) if consider_list else "無"

    return (
        f"**活動：{activity}**\n\n"
        f"**加入：** {join_str}\n"
        f"**不加入：** {not_join_str}\n"
        f"**考慮加入：** {consider_str}"
    )

def create_buttons(activity: str) -> View:
    """建立加入、不加入、考慮加入的按鈕"""
    join_button = Button(label="加入", style=discord.ButtonStyle.green)
    not_join_button = Button(label="不加入", style=discord.ButtonStyle.red)
    consider_button = Button(label="考慮加入", style=discord.ButtonStyle.grey)

    async def join_callback(interaction: discord.Interaction):
        user = interaction.user.name
        if user in memo_data[activity]["not_join"]:
            memo_data[activity]["not_join"].remove(user)
        if user in memo_data[activity]["consider"]:
            memo_data[activity]["consider"].remove(user)
        if user not in memo_data[activity]["join"]:
            memo_data[activity]["join"].append(user)
        await interaction.response.edit_message(content=generate_memo_message(activity), view=create_buttons(activity))

    async def not_join_callback(interaction: discord.Interaction):
        user = interaction.user.name
        if user in memo_data[activity]["join"]:
            memo_data[activity]["join"].remove(user)
        if user in memo_data[activity]["consider"]:
            memo_data[activity]["consider"].remove(user)
        if user not in memo_data[activity]["not_join"]:
            memo_data[activity]["not_join"].append(user)
        await interaction.response.edit_message(content=generate_memo_message(activity), view=create_buttons(activity))

    async def consider_callback(interaction: discord.Interaction):
        user = interaction.user.name
        if user in memo_data[activity]["join"]:
            memo_data[activity]["join"].remove(user)
        if user in memo_data[activity]["not_join"]:
            memo_data[activity]["not_join"].remove(user)
        if user not in memo_data[activity]["consider"]:
            memo_data[activity]["consider"].append(user)
        await interaction.response.edit_message(content=generate_memo_message(activity), view=create_buttons(activity))

    join_button.callback = join_callback
    not_join_button.callback = not_join_callback
    consider_button.callback = consider_callback

    view = View()
    view.add_item(join_button)
    view.add_item(not_join_button)
    view.add_item(consider_button)
    return view

def setup(bot):
    bot.add_cog(MemoCog(bot))
