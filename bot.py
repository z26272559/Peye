import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
intents.voice_states = True

OWNER_ID = 593426927394488357
TOKEN = "MTI0NjA1NTgyOTY4MjEyNjkzOQ.Gomiit.GIdFhOrYZyKy6fy3pkp6UhRJY_7xGa8K102xVY"
# 禁用內建的 help 指令
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, help_command=None)

# Cog 名稱列表
cogs = ["memo", "vote", "roll", "help","steam"]

# 加載所有 Cog
for cog in cogs:
    bot.load_extension(f"cogs.{cog}")

@bot.event
async def on_ready():
    print(f'Bot 已啟動，登入為 {bot.user}')

@bot.command()
async def load(ctx, extension: str):
    """加載指定的Cog"""
    if ctx.author.id == OWNER_ID:
        try:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"成功加載 {extension} Cog！")
        except Exception as e:
            await ctx.send(f"加載 {extension} Cog 時發生錯誤：{e}")
    else:
        await ctx.send("你沒有權限執行這個指令！")

# 卸載指定的Cog
@bot.command()
async def unload(ctx, extension: str):
    """卸載指定的Cog"""
    if ctx.author.id == OWNER_ID:
        try:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"成功卸載 {extension} Cog！")
        except Exception as e:
            await ctx.send(f"卸載 {extension} Cog 時發生錯誤：{e}")
    else:
        await ctx.send("你沒有權限執行這個指令！")

# 重新加載指定的Cog
@bot.command()
async def reload(ctx, extension: str):
    """重新加載指定的Cog"""
    if ctx.author.id == OWNER_ID:
        try:
            bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"成功重新加載 {extension} Cog！")
        except Exception as e:
            await ctx.send(f"重新加載 {extension} Cog 時發生錯誤：{e}")
    else:
        await ctx.send("你沒有權限執行這個指令！")

bot.run(TOKEN)
