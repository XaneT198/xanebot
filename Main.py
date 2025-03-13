import discord
from discord.ext import commands
import os
import requests
import random   
import time

intents = discord.Intents.all()
intents.message_content = True

Token = os.getenv("TOKEN")
Tenkey = os.getenv("TENKEY")
searchterm = "Funny meme"

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Hey {bot.user} is online")
    print(Tenkey)
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

@bot.command() 
async def MemCount(ctx):
    guild = ctx.guild
    await ctx.send(f'{guild.name} has {guild.member_count} members.')

@bot.command()
async def randGIF(ctx, *, search_term):
    url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={Tenkey}&limit=10"
    response = None

    try:
        response = response.get(url)
        response.raise_for_status()
        gifs = response.json().get("Results")

        if gifs:
            random_gif = random.choice(gifs)["url"]
            await ctx.send(random_gif)
        else:
            await ctx.send("No available gifs man :(")
    
    except requests.exceptions.RequestException as e:
        await ctx.send("Couldn't get any gifs call xane")
        print(f'request failed: {e}')


    except Exception as e:
        await ctx.send("call xane im fucked up")
        print(f'request failed: {e}')




bot.run(Token)
