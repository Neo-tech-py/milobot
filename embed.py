from discord.ext import commands
import discord
import random
import datetime
import sqlite3

# These color constants are taken from discord.js library
colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}


class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
    	db = sqlite3.connect('main.sqlite')
    	cursor = db.cursor()
    	cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
    	result = cursor.fetchone()
    	if result is None:
    		return
    	else:
    		cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
    		result1 = cursor.fetchone()
    		members = len(list(member.guild.members))
    		mention = member.mention
    		user = member.name
    		guild = member.guild
    		embed = discord.Embed(color=discord.Color.dark_green(), description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild), timestap=datetime.datetime.utcfromtimestamp(1553629094))
    		embed.set_thumbnail(url=f"{member.avatar_url}")
    		embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    		embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    		embed.timestamp = datetime.datetime.utcnow()
    		
    		channel = self.client.get_channel(int(result[0]))
    		await channel.send(embed=embed)
    	
    @commands.group(invoke_without_command=True)
    async def welcomer(self, ctx):
    	await ctx.send('**Available Setup Commands:** welcomer set_channel <#channel> & welcomer text <text>')
    	
    @welcomer.command()
    async def set_channel(self, ctx, channel:discord.TextChannel):
    	if ctx.message.author.guild_permissions.manage_messages:
    		db = sqlite3.connect('main.sqlite')
    		cursor = db.cursor()
    		cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
    		result = cursor.fetchone()
    		if result is None:
    			sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?, ?)")
    			val = (ctx.guild.id, channel.id)
    			await ctx.send(f"Welcome channel set to **{channel.mention}**")
    		elif result is not None:
    			sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
    			val = (channel.id, ctx.guild.id)
    			await ctx.send(f"Welcome channel updated to **{channel.mention}**")
    		cursor.execute(sql, val)
    		db.commit()
    		cursor.close()
    		db.close()
    		
    @welcomer.command()
    async def set_text(self, ctx, *, text):
    	if ctx.message.author.guild_permissions.manage_messages:
    		db = sqlite3.connect('main.sqlite')
    		cursor = db.cursor()
    		cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
    		result = cursor.fetchone()
    		if result is None:
    			sql = ("INSERT INTO main(guild_id, msg) VALUES(?, ?)")
    			val = (ctx.guild.id, text)
    			await ctx.send(f"Welcome message set to **{text}**")
    		elif result is not None:
    			sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
    			val = (text, ctx.guild.id)
    			await ctx.send(f"Welcome message updated to **{text}**")
    		cursor.execute(sql, val)
    		db.commit()
    		cursor.close()
    		db.close()

    @commands.command(
        name='embed',
        description='The embed command',
    )
    async def embed_command(self, ctx):

        # Define a check function that validates the message received by the bot
        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        # First ask the user for the title
        await ctx.send(content='What would you like the title to be?')

        # Wait for a response and get the title
        msg = await self.client.wait_for('message', check=check)
        title = msg.content # Set the title

        # Next, ask for the content
        await ctx.send(content='What would you like the Description to be?')
        msg = await self.client.wait_for('message', check=check)
        desc = msg.content

        # Finally make the embed and send it
        msg = await ctx.send(content='Now generating the embed...')

        color_list = [c for c in colors.values()]
        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=title,
            description=desc,
            color=random.choice(color_list)
        )
        # Also set the thumbnail to be the bot's pfp
        embed.set_thumbnail(url=self.client.user.avatar_url)

        # Also set the embed author to the command user
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await msg.edit(
            embed=embed,
            content=None
        )
        # Editing the message
        # We have to specify the content to be 'None' here
        # Since we don't want it to stay to 'Now generating embed...'

        return


def setup(client):
	client.add_cog(Embed(client))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has