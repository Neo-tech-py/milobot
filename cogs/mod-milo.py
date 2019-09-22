import discord
from discord.ext import commands
from cogs.utils import checks

class Moderation(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		guild = channel.guild
		role = discord.utils.get(guild.roles, name = "Muted")
		if role == None:
			role = await guild.create_role(name = "Muted")
		await channel.set_permissions(role, send_messages = False)
		
	@commands.command()
	@commands.has_permissions(kick_members=True)
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
		await ctx.channel.send(f"{member} has been kicked out by {ctx.author.name}", delete_after = 5.0)
		
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❗You Dont have Permission to kick")
		
	@commands.command()
	@commands.has_permissions(ban_members=True)
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
		await ctx.send(f"{member} has been banned by **{ctx.author.name}**", delete_after = 5.0)
		
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You Dont have permission to ban")
		
	@commands.command()
	@commands.has_permissions(ban_members=True)
	@checks.is_mod()
	async def unban(self, ctx, *, member: discord.User = None):
		if member == None:
			embed = discord.Embed(color=0xc80afc, title="Unban Error", description="Please mention a user to unban")
			await ctx.send(embed=embed, delete_after = 5.0)
		else:
			banned_users = ctx.guild.bans()
			for ban_entry in banned_users:
				user = ban_entry.user
				
				if (user.name, user.discriminator) == (member.name, member.discriminator):
					embed = discord.Embed(color=0x62ff00, title="Unban", description=f"{user.mention} has been unbanned")
					await ctx.guild.unban(user)
					await ctx.send(embed=embed, delete_after = 5.0)
					
	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You Dont have permission to unban")

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	@checks.is_mod()
	async def purge(self, ctx, amount = 10):
		max = 2000
		if amount >= 1 and amount <= max:
			await ctx.channel.purge(limit = amount + 1)
			embed = discord.Embed(color=0xff0059, title="Purge", description=f"{amount} has been Purged!")
			await ctx.send(embed=embed, delete_after = 5.0)
			
	@purge.error
	async def purge_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You dont have Permission to purge")
			
	@commands.command()
	@commands.has_permissions(kick_members=True)
	@checks.is_mod()
	async def mute(self, ctx, member: discord.Member = None, *, reason = None):
		if member == None:
			embed = discord.Embed(color=discord.Color.dark_red(), title="Mute Error", description="You have to specify a member to mute")
			await ctx.send(embed=embed, delete_after = 5.0)
		else:
			if member.id == ctx.message.author.id:
				embed = discord.Embed(color=discord.Color.greyple(), title="Mute Error", description="You Cannot mute yourself")
				await ctx.send(embed=embed, delete_after = 5.0)
			else:
				if reason == None:
					role = discord.utils.get(ctx.guild.roles, name = "Muted")
					if role == None:
						role = await ctx.guild.create_role(name = "Muted")
						for channel in ctx.guild.text_channels:
							await channel.set_permissions(role, send_messages = False)
					await member.add_roles(role)
					embed = discord.Embed(color=0x7289DA, title="Mute", description=f"{member.mention} has been muted by {ctx.message.author.mention}.\nReason - {reason}")
					await ctx.send(embed=embed, delete_after = 5.0)
					
	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You dont have Permission to mute")
					
	@commands.command()
	@commands.has_permissions(kick_members=True)
	@checks.is_mod()
	async def unmute(self, ctx, member: discord.Member = None):
		if member == None:
			embed = discord.Embed(color=0xFF2B2B, title="Unmute Error", description="You have to mention a member to unmute")
			await ctx.send(embed=embed, delete_after = 5.0)
		else:
			role = discord.utils.get(ctx.guild.roles, name = "Muted")
			if role in member.roles:
				await member.remove_roles(role)
				embed = discord.Embed(color=0x7289DA, title="Unmute", description=f"{member.mention} has been unmuted by {ctx.message.author.mention}")
				await ctx.send(embed=embed, delete_after = 5.0)
				
	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You dont have permission to unmute")
				
	@commands.command()
	@commands.has_permissions(ban_members=True)
	@checks.is_mod()
	async def softban(self, ctx, member: discord.Member = None, *, reason = None):
		if member == None:
			embed = discord.Embed(color=0xFF2B2B, title="Softban Error", description="You have to specify a member to softban")
			await ctx.send(embed=embed, delete_after = 5.0)
		else:
			if member.id == ctx.message.id:
				embed = discord.Embed(color=	0xFF2B2B, title="Softban Error", description="You Cannot softban yourself")
				await ctx.send(embed=embed, delete_after = 5.5)
			else:
				if reason == None:
					await member.ban(reason=f"{member.mention} has been softbanned by {ctx.message.author.mention}.\nReason - {reason}")
					await member.unban()
					embed = discord.Embed(color=discord.Color.blurple, title="Softban", description=f"{member.mention} has been softbanned by {ctx.message.author.mention}.\nReason - {reason}")
					await ctx.send(embed=embed, delete_after = 10.0)
					
	@softban.error
	async def softban_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You dont have permission to do softban")
			
	@commands.command()
	@commands.has_permissions(manage_server=True)
	@checks.is_mod()
	async def nuke(self, ctx):
		channel_position = ctx.channel.position
		new_channel = await ctx.channel.clone()
		await new_channel.edit(reason=f"Nuke by {ctx.message.author.name}#{ctx.author.discriminator}", position = channel_position)
		await ctx.channel.delete()
		embed = discord.Embed(title="Nuke", description="This Channel has been Nuked!", color=discord.Color.blurple)
		embed.set_image(url="https://media.tenor.com/images/2d09f6be0116a7cac412dca839c5eda5/tenor.gif")
		await new_channel.send(embed=embed, delete_after = 30.5)
		
	@nuke.error
	async def nuke_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("❕You dont have permission to nuke")
			
def setup(client):
	client.add_cog(Moderation(client))
	print("Moderation loaded")
			