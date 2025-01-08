# cogs/vote.py
import discord
from discord.ext import commands
from discord.ui import Button, View

class VoteView(View):
    def __init__(self, options, ctx):
        super().__init__()
        self.options = options
        self.ctx = ctx
        self.voters = {option: [] for option in options} 
        self.user_votes = {}  
        for option in self.options:
            button = Button(label=option, style=discord.ButtonStyle.primary, custom_id=f"vote_option_{option}")
            button.callback = self.create_callback(option)
            self.add_item(button)

    def create_callback(self, option):
        """動態創建每個按鈕的回調函數"""
        async def callback(interaction: discord.Interaction):
            user = interaction.user.name
            if user in self.user_votes:
                old_option = self.user_votes[user]
                self.voters[old_option].remove(user)  
            self.voters[option].append(user)
            self.user_votes[user] = option  
            await interaction.response.send_message(f"{user} 已經投票給了 {option}")
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("你不能為別人投票！", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="查看投票結果", style=discord.ButtonStyle.secondary, custom_id="vote_results")
    async def show_results(self, button: Button, interaction: discord.Interaction):
        results_message = "**投票結果：**\n"
        for option, voters in self.voters.items():
            if voters:
                results_message += f"**{option}:** {', '.join(voters)}\n"
            else:
                results_message += f"**{option}:** 無\n"
        await interaction.response.send_message(results_message)


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vote(self, ctx, *options):
        """進行投票的指令"""
        if len(options) < 2:
            await ctx.send("請提供至少兩個選項進行投票！")
            return
        view = VoteView(options, ctx)
        await ctx.send(f"**投票：** {' '.join(options)}", view=view)


# 註冊 Cog
def setup(bot):
    bot.add_cog(VoteCog(bot))
