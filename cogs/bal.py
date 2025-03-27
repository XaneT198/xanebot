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

class bal(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.connect = sqlite3.connect('balances.db')
        self.cursor = self.connect.cursor()
        print("Database connected successfully.")
        self.connect.commit()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_balances (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER
        )''')
        self.connect.commit()

    @commands.command()
    async def bal(self, ctx):
        try:
            id = ctx.author.id
        
            self.cursor.execute('SELECT balance FROM user_balances WHERE user_id = ?', (id,))
            result = self.cursor.fetchone()

            if result is None:
                await ctx.send("You don't have a balance record yet! Starting with 5000 coins.")
                self.cursor.execute('INSERT INTO user_balances (user_id, balance) VALUES (?, ?)', (id, 5000))
                self.connect.commit()
                return
        
            await ctx.send(f"Your current balance is {result[0]} :moneybag:")
        except Exception as e:
            print(f"Error occurred in bal command: {e}")
            await ctx.send("There was an error fetching your balance. Please try again later.")
        

def cog_unload(self):
    self.connect.close()

async def setup(bot):
    await bot.add_cog(bal(bot))