import discord
from discord.ext import commands
import os
import requests
import random   
import time
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv("TOKEN")
GKEY = os.getenv("GKEY")
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print("Hey {bot.user} is online")
    print(GKEY)
    print(Token)


@bot.command()
async def hello(ctx):
    await ctx.send("Hey i'm xanebot programmed by Xane Thompson ")
    time.sleep(0.5)
    await ctx.send("use .how to see all of my available commands")


@bot.command()
async def how (ctx):
    await ctx.send("My Current commands are: ")
    await ctx.send(".hello - Greet me ")
    await ctx.send(".MemCount - See the current member count")
    await ctx.send(".randGIF - recieve a random gif")


@bot.command() 
async def MemCount(ctx):
    guild = ctx.guild
    await ctx.send(f'{guild.name} has {guild.member_count} members.')


@bot.command()
async def randGIF(ctx, *, query: str = "Funny"):
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



bot.run(Token)
