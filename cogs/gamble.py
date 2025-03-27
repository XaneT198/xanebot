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

class gamble(commands.Cog):  
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
    async def gamble(self, ctx, amount: int = 1000):
        id = ctx.author.id
        self.cursor.execute('SELECT balance FROM user_balances WHERE user_id = ?', (id,))
        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute('INSERT INTO user_balances (user_id, balance) VALUES (?, ?)', (id, 5000))
            self.connect.commit()
            current_balance = 5000
        else:
            current_balance = result[0]
        
        if current_balance < amount:
            return await ctx.send(embed=discord.Embed(description="You don't have enough to gamble", color=discord.Color.red()))
        
        userstrikes = random.randint(1, 14)
        botstrikes = random.randint(3, 14)

        if userstrikes > botstrikes:
            percent = random.randint(50, 100)
            amount_won = int(amount * (percent / 100))
            new_balance = current_balance + amount_won
            self.cursor.execute('UPDATE user_balances SET balance = ? WHERE user_id = ?', (new_balance, id))
            self.connect.commit()
            embed = discord.Embed(description=f"You Won **{amount_won}** :moneybag:\n"
                                              f"Percent won: **{percent}%**\n"
                                              f"New Balance: **{new_balance}** :moneybag:",
                                  color=discord.Color.random())
            embed.set_author(name=f"{ctx.author.name} is lowkey goated ngl", icon_url=ctx.author.avatar.url)

        elif userstrikes < botstrikes:
            percent = random.randint(0, 80)
            amount_lost = int(amount * (percent / 100))
            new_balance = current_balance - amount_lost
            self.cursor.execute('UPDATE user_balances SET balance = ? WHERE user_id = ?', (new_balance, id))
            self.connect.commit()
            embed = discord.Embed(description=f"you lost **{amount_lost}** :moneybag:\n"
                                              f"percent: **{percent}%**\n"
                                              f"new balance: **{new_balance}** :moneybag:",
                                  color=discord.Color.random())
            embed.set_author(name=f"{ctx.author.name} is washed asf", icon_url=ctx.author.avatar.url)

        else:
            embed = discord.Embed(description="**It was a tie**", color=discord.Color.random())
            embed.set_author(name="Tie", icon_url=ctx.author.avatar.url)
            embed.add_field(name=f"**{ctx.author.name.title()}**", value=f"Strikes {userstrikes}")
            embed.add_field(name=f"**{self.bot.user.name.title()}**", value=f"Strikes {botstrikes}")
            embed.timestamp = datetime.datetime.utcnow()  

        await ctx.send(embed=embed)
        
def cog_unload(self):
    self.connect.close()

async def setup(bot):
    await bot.add_cog(gamble(bot))
