import discord
import asyncio
from discord.ext import commands
import sqlite3
import random
import time
from dotenv import load_dotenv
import datetime
import re

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connect = sqlite3.connect('balances.db')
        self.cursor = self.connect.cursor()
        self.connect.commit()

        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_balances (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER
        )''')
        self.connect.commit()

    @commands.command()
    async def work(self, ctx):
        id = ctx.author.id
        

        self.cursor.execute('SELECT balance FROM user_balances WHERE user_id = ?', (id,))
        result = self.cursor.fetchone()

      
        if result is None:
            await ctx.send("You don't have a balance record yet! Starting with 5000 coins.")
            self.cursor.execute('INSERT INTO user_balances (user_id, balance) VALUES (?, ?)', (id, 5000))
            self.connect.commit()
            return

    
        current_balance = result[0]
        new_balance = current_balance + 300

        self.cursor.execute('UPDATE user_balances SET balance = ? WHERE user_id = ?', (new_balance, id))
        self.connect.commit()
        
       
        await ctx.send(f"Good work! You've earned 300 coins. Your new balance is {new_balance} :moneybag:")

    def cog_unload(self):
        self.connect.close()

async def setup(bot):
    await bot.add_cog(work(bot))
