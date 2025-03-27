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

load_dotenv()
Token = os.getenv("Token")
GKEY = os.getenv("GKEY")

async def load_extensions():
    await bot.load_extension("cogs.how")
    await bot.load_extension("cogs.hello")
    await bot.load_extension("cogs.memcount")
    await bot.load_extension("cogs.gamble")
    await bot.load_extension("cogs.randgif")
    await bot.load_extension("cogs.bal")  
    await bot.load_extension("cogs.work")
    await bot.load_extension("cogs.leaderboard")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Hey {bot.user} is online")
    print(GKEY)
    print(Token)
    await bot.tree.sync()

async def main():
    await load_extensions()
    await bot.start(Token)

asyncio.run(main())
