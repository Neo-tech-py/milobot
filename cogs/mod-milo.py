import discord
from discord.ext import commands
from cogs.utils import checks

class Moderation(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		
	@commands.command()
	@checks.is_mod()
	async def kick(self, ctx, member : discord.Member = None, reason = None):
		if member == None:
			await ctx.send(f"Please Select A **Member** to kick {ctx.author.mention}")
		if member == ctx.message.author:
			await ctx.send(f"You Cannot Kick Yourself {ctx.author.mention}")
		if reason == None:
			reason = f"Please Specify a reason to kick {ctx.author.mention}"
		message = f"You Have Been kicked Out from **{ctx.guild.name}**, Kicked by : {ctx.author.name}"
		await member.send(message)
		await ctx.guild.kick(member)
		await ctx.channel.send(f"{member} has been kicked out by {ctx.author.name}")
		
	@commands.command()
	@checks.is_mod()
	async def ban(self, ctx, member : discord.Member = None, reason = None):
		if member == None:
			await ctx.send(f"Please specify a **member** to ban {ctx.author.mention}")
		if member == ctx.message.author:
			await ctx.send(f"You cannot ban yourself {ctx.message.author} `lol`")
		if reason == None:
			await ctx.send(f"Please give a reason to ban the member **{ctx.author.name}**")
		message = f"You have been banned from {ctx.guild.name} | Action done by {ctx.message.author.name}"
		await member.send(message)
		await ctx.send(f"{member} has been banned by **{ctx.author.name}**")
		
def setup(client):
	client.add_cog(Moderation(client))
	print("Moderation has been loaded")
			