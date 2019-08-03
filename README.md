![Logo](https://i.imgur.com/4ims2Lc.png)

# What is MiloBot?
An easy to use And fun to use discord bot. Milo is the Simple and funny discord bot which can be used to do moderation, Economy, Fun, Game.

# How to self-host the bot?
Self Host can be done via heroku. The steps to host and complete guide in wiki

# What about Contribution?
Contribution is hearty welcomed. Send your code via [Pull Requests](https://github.com/Neo-tech-py/milobot/pulls), and in E-Mail - imgroot078@gmail.com. If your Code runs perfectly we will merge it give a special role in our discord server.

# Example code for newbies!!
**Install Modules first**
```sh
#Windows
py3 -m pip install -U discord.py
#Linux
python-3 -m pip install -U discord.py
#Voice Support
#Windows
py-3 -m pip install -U discord.py[voice]
#Linux
python-3 -m pip install -U discord.py[voice]
```

**A Example Bot Code for Your Own Command**

```py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="-")

@bot.event
async def on_ready():
  print('Bot is Ready')
  
@bot.command()
 async def ping(ctx):
   await ctx.send('**Pong!**')
   
 bot.run('TOKEN') # TODO: Insert Bot token
 ```
 **Cogs Example**
 Cogs are used to arrange your commands
 
```py
#Please see discord.py documentation for more info
import discord
from discord.ext import commands

#Cogs Must derive from Cog
class Example(commands.Cog):

  def __init__(self, bot)
  self.bot == bot
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Done')
    
  @commands.command(name="Ping", description="Return Pong", hidden=False)#Set this to true if you want to hide it
  async def ping(self, ctx):
    await ctx.send('**Pong!**')
    
def setup(bot):
  client.add_cog(Example(bot))
  ```
**These Are the some Examples You can find more in discord.py documentation**

_I Wish you would make your own code for your bot using this example_

# External Link

* [discord.py documentation](https://discordpy.readthedocs.io/en/latest/)
* [Patreon](https://patreon.com/PrabaRock7)
* [License](https://github.com/Neo-tech-py/milobot/blob/master/LICENSE)

*** 




















