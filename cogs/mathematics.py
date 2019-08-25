import discord
from discord.ext import commands

class Mathematics(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def add(self, ctx, left : int, right : int):
		await ctx.send(left + right)
		
	@commands.command()
	async def subtract(self, ctx, left : int, right : int):
		await ctx.send(left - right)
		
	@commands.command()
	async def multiply(self, ctx, left : int, right : int):
		await ctx.send(left * right)
		
	@commands.command()
	async def divide(self, ctx, left : int, right : int):
		await ctx.send(left / right)
		
def setup(client):
	client.add_cog(Mathematics(client))