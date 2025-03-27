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
import sqlite3

import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime

class leaderboard(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.connect = sqlite3.connect('balances.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_balances (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER
        )''')
        self.connect.commit()

    @commands.command()
    async def leaderboard(self, ctx):
        
        self.cursor.execute('SELECT user_id, balance FROM user_balances ORDER BY balance DESC LIMIT 3')
        leaderboard = self.cursor.fetchall()

        if not leaderboard:
            await ctx.send("No leaderboard data available.")
            return

    
        embed = discord.Embed(title="Top 3 Leaderboard", description="Here are the top 3 users with the highest balances", color=discord.Color.blue())

    
        for i, (user_id, balance) in enumerate(leaderboard, 1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"**#{i} {user.name}**", value=f"Balance: **{balance}** :moneybag:", inline=False)

        await ctx.send(embed=embed)

    def cog_unload(self):
        self.connect.close()

async def setup(bot):
    await bot.add_cog(leaderboard(bot))
