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
        await ctx.send(".hello - Greet me ")
        await ctx.send(".memcount - See the current member count")
        await ctx.send(".randGIF - recieve a random gif")
        await ctx.send(".gamble - gamble to gain a higher place on the leaderbord")

async def setup(bot):
    await bot.add_cog(how(bot))