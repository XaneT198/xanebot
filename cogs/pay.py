import discord
import asyncio
from discord.ext import commands
import sqlite3
import datetime

class pay(commands.Cog):
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
    async def pay(self, ctx, member: discord.Member, amount: int):
        sender_id = ctx.author.id
        receiver_id = member.id

        if amount <= 0:
            return await ctx.send(embed=discord.Embed(description="Please enter a positive amount to transfer.", color=discord.Color.red()))

        # Retrieve sender's balance
        self.cursor.execute('SELECT balance FROM user_balances WHERE user_id = ?', (sender_id,))
        sender_balance = self.cursor.fetchone()

        # Retrieve receiver's balance
        self.cursor.execute('SELECT balance FROM user_balances WHERE user_id = ?', (receiver_id,))
        receiver_balance = self.cursor.fetchone()

        if sender_balance is None:
            self.cursor.execute('INSERT INTO user_balances (user_id, balance) VALUES (?, ?)', (sender_id, 2000))
            self.connect.commit()
            sender_balance = (2000,)

        if receiver_balance is None:
            self.cursor.execute('INSERT INTO user_balances (user_id, balance) VALUES (?, ?)', (receiver_id, 2000))
            self.connect.commit()
            receiver_balance = (2000,)

        sender_balance = sender_balance[0]
        receiver_balance = receiver_balance[0]

        if sender_balance < amount:
            return await ctx.send(embed=discord.Embed(description="You don't have enough to send.", color=discord.Color.red()))

        # Send request to receiver
        request_embed = discord.Embed(
            description=f"**{ctx.author.name}** is trying to send you **{amount}** :moneybag:\n\n"
                        "Do you want to accept this payment?",
            color=discord.Color.blue())
        request_embed.set_footer(text="React with 👍 to accept or 👎 to decline.")
        try:
            request_message = await member.send(embed=request_embed)
            await request_message.add_reaction('👍')
            await request_message.add_reaction('👎')

            def check_reaction(reaction, user):
                return user == member and str(reaction.emoji) in ['👍', '👎'] and reaction.message.id == request_message.id

            # Wait for the reaction (timeout after 60 seconds)
            reaction, user = await self.bot.wait_for('reaction_add', check=check_reaction, timeout=60.0)

            if str(reaction.emoji) == '👍':
                new_sender_balance = sender_balance - amount
                new_receiver_balance = receiver_balance + amount

                self.cursor.execute('UPDATE user_balances SET balance = ? WHERE user_id = ?', (new_sender_balance, sender_id))
                self.cursor.execute('UPDATE user_balances SET balance = ? WHERE user_id = ?', (new_receiver_balance, receiver_id))
                self.connect.commit()

                embed = discord.Embed(
                    description=f"**{ctx.author.name}** sent **{amount}** :moneybag: to **{member.name}**.\n"
                                f"Your new balance: **{new_sender_balance}** :moneybag:\n"
                                f"{member.name}'s new balance: **{new_receiver_balance}** :moneybag:",
                    color=discord.Color.green())
                embed.set_author(name="Payment Successful", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                await member.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(description="The payment has been declined.", color=discord.Color.red()))
                await member.send(embed=discord.Embed(description="You declined the payment.", color=discord.Color.red()))

        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(description="The payment request timed out. Payment cancelled.", color=discord.Color.red()))
            await member.send(embed=discord.Embed(description="The payment request timed out. Payment cancelled.", color=discord.Color.red()))

    def cog_unload(self):
        self.connect.close()

async def setup(bot):
    await bot.add_cog(pay(bot))
