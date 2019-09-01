__version__ = "1.0.0"
__owner__ = "PrabaRock7"
__c__ = "PrabaRock7© 2019-2020"
__license__ = "MIT LICENSE"

import discord
from discord.ext import commands
from cogs.utils import checks, default, perms, repo
import logging
import random
import os
import typing
import json
import datetime
import aiohttp
import sqlite3
import sys
import traceback
import asyncio

client = commands.Bot(
           command_prefix="%",
           description="MiloBot",
           owner_id=589647651939549206,
           case_insensitive=True
)
client.remove_command('help')

@client.command(name="load", discription="Loads a cog", hidden=True)
@checks.is_creator()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")
	await ctx.send('Successfully loaded')
	
@client.command(hidden=True)
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	await ctx.send('Successfully unloaded')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name + '#' + client.user.discriminator)
	print("v%s", __version__, __c__, __owner__)
	
@client.event
async def on_command_error(ctx, error):
	embed = discord.Embed(title=f"An error Occured", description=f"{error}", color=discord.Color.dark_magenta())
	await ctx.send(embed=embed)
	
@client.command()
async def help(ctx):
	embed = discord.Embed(title="An Imteractive Help Command to solve your Queries", description="List of all Commands", color=discord.Color.dark_teal(), timestap=datetime.datetime.utcnow())
	embed.add_field(name="General Commands", value="*ping | avatar | userinfo | guildinfo | welcomer | embed | bitcoin | serverstats*")
	embed.add_field(name="Mathematics Commands", value="*add | subtract | multiply | divide*")
	embed.add_field(name="Fun Commands", value="*meme | slap | echo | mentionme | cat*")
	embed.add_field(name="Action Commands", value="*ban | unban | kick | purge*")
	await ctx.send(embed=embed)
	
@client.command()
async def welcomer_help(ctx):
	msg = "Available Setup Commands are `welcomer set_channel` - **Set the welcome channel** and `welcomer set_text` - **Set the message for welcome**.Available Formats : `{user}` - **Shows the member name**, `{mention}` - **Mentions the user**, `{members}` - **Shows the list of members**, `{guild}` - **Shows the guild name**"
	await ctx.send(msg)
			
class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

@client.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)
	
@client.command(hidden=True)
@commands.is_owner()
async def logout(ctx):
	print('Logged Out')
	async with ctx.typing():
		await ctx.send("Logged out successfully")
		await client.logout()
		print('Done')
		
@client.command(hidden=True)
@commands.is_owner()
async def connect(ctx):
	print("Connecting...")
	await client.connect(reconnect=True)
	print("Connected" + (len(client.guilds)))
	
@client.command()
async def ping(ctx):
	await ctx.send(f"Pong! | My latency is {round(client.latency * 1000)}ms")
	
@client.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
    
@client.command()
async def avatar(ctx):
	show_avatar = discord.Embed(
	
	         color = discord.Color.blue()
	)
	show_avatar.set_image(url="{}".format(ctx.author.avatar_url))
	await ctx.author.send(embed=show_avatar)
	
@client.command()
async def userinfo(ctx, member: discord.Member):
	roles = [role for role in member.roles]
	
	em = discord.Embed(title=f"Userinfo - {member.name}", description=f"Shows Info about {member.name}", color=discord.Color.dark_orange(), timestap=datetime.datetime.utcfromtimestamp(1553629094))
	em.set_thumbnail(url=f"{member.avatar_url}")
	em.add_field(name="ID:", value=member.id)
	em.add_field(name="Guild_Name:", value=member.display_name)
	
	em.add_field(name="Created_at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name="Joined_at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
	em.add_field(name="Top Role", value=member.top_role.mention)
	em.add_field(name="Bot?", value=member.bot)
	
	await ctx.send(embed=em)
	
@client.command()
async def guildinfo(ctx):
	roles = [role for role in ctx.guild.roles]
	guild_age = (ctx.message.created_at - ctx.author.guild.created_at).days
	created_at = f"Server created on {ctx.author.guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
	online = len({m.id for m in ctx.author.guild.members if m.status is not discord.Status.offline})
	em = discord.Embed(title=f"Guild Info - {ctx.guild.name}", description=created_at, color=discord.Color.blurple())
	em.set_thumbnail(url=ctx.author.guild.icon_url)
	em.set_author(name="Guild Info", icon_url=ctx.author.guild.icon_url)
	em.add_field(name="Name:", value=ctx.author.guild.name)
	em.add_field(name="Id:", value=ctx.author.guild.id)
	em.add_field(name="Online:", value=online)
	em.add_field(name="Total Members:", value=len(ctx.author.guild.members))
	em.add_field(name="Owner:", value=ctx.guild.owner)
	em.add_field(name="Roles:", value=len(roles))
	em.add_field(name="Emojis:", value=len(ctx.guild.emojis))
	em.add_field(name="Region", value=ctx.guild.region)
	em.add_field(name="Verification level", value=ctx.guild.verification_level)
	em.add_field(name="Text Channels:", value=ctx.guild.text_channels)
	em.add_field(name="Voice Channs:", value=ctx.guild.voice_channels)
	await ctx.send(embed=em)
	
@client.command()
async def meme(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.reddit.com/r/me_irl/random") as r:
			data = await r.json()
			await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
			
@client.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command()
async def cat(ctx):
	msg = "https://moderncat-wpengine.netdna-ssl.com/sites/default/files/images/uploads/ScienceKittens.gif"
	await ctx.send(msg)

@client.command()
async def echo(ctx, amount: int, *, message):
	if amount <= 5:
		for i in range(amount):
			await ctx.send(message)
	else:
		await ctx.send("Please use a number less or equal to 5")

@client.command()
async def mentionme(ctx):
	await ctx.send(ctx.author.mention + "Mentioned You")
	
@client.command()
async def serverstats(ctx):
	bots = 0
	members = 0
	total = 0
	for x in ctx.guild.members:
		if x.bot == True:
			bots += 1
			total += 1
		else:
			members += 1
			total += 1
	embed = discord.Embed(title="Server Stats", color=discord.Color.dark_red())
	embed.add_field(name="Bot Count", value=f'{bots}', inline=True)
	embed.add_field(name="Member Count", value=f'{members}', inline=True)
	embed.add_field(name="Total Count", value=f'{total}', inline=True)
	await ctx.send(embed=embed)
	
async def change_pr():
	await client.wait_until_ready()
	
	statuses = ["%help", "Playing on guilds : " + str(len(client.guilds)), "Used by Users : " + str(len(client.users))]
	
	while not client.is_closed():
		status = random.choice(statuses)
		
		await client.change_presence(activity=discord.Game(status))
		
		await asyncio.sleep(2)
	
client.loop.create_task(change_pr())
client.run(os.getenv("TOKEN"))