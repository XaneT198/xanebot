import discord
from discord.ext import commands
import os
import time

intents = discord.Intents.all()
intents.message_content = True

Token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Hey {bot.user} is online")

@bot.command()
async def hello(ctx):
    await ctx.send("Hey i'm xanebot programmed by Xane Thompson ")
    time.sleep(0.5)
    await ctx.send("use .list to see all of my available commands")

@bot.command()
async def list (ctx):
    await ctx.send("My Current commands are: ")
    await ctx.send(".hello - Greet me ")
    await ctx.send(".MemCount - See the current member count")

@bot.command() 
async def MemCount(ctx):
    guild = ctx.guild
    await ctx.send(f'{guild.name} has {guild.member_count} members.')



bot.run(Token)
