import discord
import asyncio
from discord.ext import commands
import os
import requests
import random   
import time
from dotenv import load_dotenv
import datetime
import re

GKEY = os.getenv("GKEY")


class randgif (commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def randgif(self,ctx, *, query: str = "Funny"):
        await ctx.send("Here you go")
        try:
            url = f'https://api.giphy.com/v1/gifs/search'
            params = {
            "api_key": GKEY,
            "q": query,
            "limit": 10
            }
            response = requests.get(url, params = params)
            data = response.json()

            if data["data"]:
                gif_url= random.choice(data["data"])["images"]["original"]["url"]
                await ctx.send(gif_url)
            else:
                await ctx.send("No GIF's Found")
        except Exception as e:
            await ctx.send(f"Call xane im fucking tweaking and {e}")

async def setup(bot):
    await bot.add_cog(randgif(bot))