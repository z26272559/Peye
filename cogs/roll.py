# cogs/roll.py
import random
from discord.ext import commands

class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, dice: str):
        """擲骰子指令"""
        try:
            number, sides = dice.upper().split("D")
            number = int(number)
            sides = int(sides) 
            if number <= 0 or sides <= 0:
                await ctx.send("骰子的數量和面數必須是正整數！")
                return
            rolls = [random.randint(1, sides) for _ in range(number)]
            total = sum(rolls)
            result = ", ".join(map(str, rolls))
            await ctx.send(f"🎲 你擲出了：{result} | 總和：{total}")
        except ValueError:
            await ctx.send("請輸入正確的格式，例如：!roll 1D10")

# 註冊 Cog
def setup(bot):
    bot.add_cog(RollCog(bot))