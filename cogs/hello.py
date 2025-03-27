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

class hello (commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hello(self,ctx):
        await ctx.send("Hey i'm xanebot programmed by Xane Thompson ")
        time.sleep(0.5)
        await ctx.send("use .how to see all of my available commands")

async def setup(bot):
    await bot.add_cog(hello(bot))