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


class memcount(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def memcount(self,ctx):
        guild = ctx.guild
        await ctx.send(f'{guild.name} has {guild.member_count} members.')

async def setup(bot):
    await bot.add_cog(memcount(bot))