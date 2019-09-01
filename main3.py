import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import aiohttp
import asyncio
import json

def get_pre(bot, message):
	prefixes = ['::', '%', '*']
	if not message.guild:
		return '**'
	return commands.when_mentioned_or(*prefixes)(bot, message)
	
bot = commands.Bot(command_prefix=get_pre, description="Easy to Handle, Fun To Use")

@bot.event
async def on_ready():
	print("Logging...")
	print("Creating Database..")
	print("Completed with no errors")
	print("Logged in")

@bot.command()
async def meme(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.reddit.com/r/me_irl/random") as r:
			data = await r.json()
			await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
			
bot.run("NjE3NTQ3ODEwMjI0NjAzMTU2.XWsuQw.rINnsLaasPH_6cnFRx1-NgPB7PU")