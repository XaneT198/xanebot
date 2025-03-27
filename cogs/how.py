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

class how(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def how (self,ctx):
        await ctx.send("My Current commands are: ")
        await ctx.send(""".hello - Greet me \n.memcount - See the current member count \n.randgif - recieve a random gif \n.gamble - gamble to potentially earn bux and move higher on the leaderbord \n.work - work and be given 300 bux \n.bal - view your balance and se ehow many credits you have \n.leaderboard - view the top 3 highest balances \n .pay - pay a specified member a certain amount of your choosing if your feeling generous :moneybag: .pay [@user] [Amount] \n .request - request a certain amount of money from a user .request [@user][Amount]""")
    

async def setup(bot):
    await bot.add_cog(how(bot))