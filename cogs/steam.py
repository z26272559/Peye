import discord
from discord.ext import commands
import requests

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://store.steampowered.com/api/appdetails"
        self.search_url = "https://store.steampowered.com/api/storesearch/"
        self.headers = {"User-Agent": "Discord Bot"}

    @commands.command()
    async def steam(self, ctx, *, game_name: str):
        """查詢 Steam 遊戲資訊"""
        try:
            # 搜索遊戲，支援中文名稱
            search_params = {
                "term": game_name,
                "l": "zh-tw",  # 搜索結果返回繁體中文
                "cc": "TW",  # 使用台灣區域
            }
            search_response = requests.get(self.search_url, params=search_params, headers=self.headers)
            search_data = search_response.json()

            if not search_data.get("items"):
                await ctx.send(f"找不到名稱為 `{game_name}` 的遊戲，請確認名稱是否正確！")
                return

            # 獲取第一個搜尋結果
            game = search_data["items"][0]
            appid = game["id"]
            title_en = game["name"]
            title_zh = game.get("localized_name", title_en)  # 如果無中文名，使用英文名
            game_thumbnail = game.get("tiny_image")

            # 獲取遊戲詳細資訊
            game_details_response = requests.get(
                f"{self.api_url}/?appids={appid}&cc=TW&l=zh-tw",
                headers=self.headers
            )
            game_details_data = game_details_response.json()

            if not game_details_data[str(appid)]["success"]:
                await ctx.send(f"無法獲取遊戲 `{game_name}` 的詳細資訊！")
                return

            details = game_details_data[str(appid)]["data"]
            is_free = details.get("is_free", False)
            price_info = details.get("price_overview", {})

            # 準備嵌入式訊息
            embed = discord.Embed(title=f"{title_zh}", color=discord.Color.blue())
            embed.set_thumbnail(url=game_thumbnail)
            
            if is_free:
                embed.add_field(name="價格", value="這是免費遊戲！", inline=False)
            else:
                original_price = price_info.get("initial", 0) / 100
                discounted_price = price_info.get("final", 0) / 100
                discount_percent = price_info.get("discount_percent", 0)

                if discount_percent > 0:
                    embed.add_field(name="原價", value=f"{original_price:.2f} TWD", inline=True)
                    embed.add_field(name="折扣", value=f"-{discount_percent}%", inline=True)
                    embed.add_field(name="折扣後價格", value=f"{discounted_price:.2f} TWD", inline=False)
                else:
                    embed.add_field(name="價格", value=f"{original_price:.2f} TWD\n目前沒有折扣。", inline=False)

            # 發送嵌入式訊息
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"發生錯誤：{e}")

def setup(bot):
    bot.add_cog(SteamCog(bot))
