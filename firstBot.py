# imports
import discord
from discord.ext import commands, tasks
import os
import random
from itertools import cycle

#create instance of a bot
# needs to stay consistent
client = commands.Bot(command_prefix='.')  #can have it set with anything
status = cycle (['Liverpool losing this season','Bayern Munich winning the UCL','The Sidemen','Ole Gunnar doing nonsense'])

# bot activation notification
@client.event
async def on_ready():  # when bot is ready to start (common)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Matrix")) 
    print('I have been activated')

# loop that updates status of bot
@tasks.loop(seconds = 10)
async def change_bot_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

# new member noti
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')
    # you can add codes here
    # for example adding him to DB or display help.join message


# memeber left noti
@client.event
async def on_member_remove(member):
    print(f"Sayonara{member}! We'll miss you~~~~~")


# commands is code triggered when users asks it to
@client.command()
# the commands can be set to do anything
async def ping(ctx):  #if user enters command ".ping"
    await ctx.send(f"Ya mudda {round(client.latency * 1000, 2)}ms"
                   )  # bot will respond with bot


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
        "You may rely on it.", "As I see it, yes.", "Most likely.",
        "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# clear chat command
# by default it will delete 5 message
# bot will clear however much user specifies
# bot will clear however much user specifies
@client.command()
@commands.has_any_role('Mod', 'Admin')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


# Kicking someone with a reason
@client.command()
@commands.has_any_role('Mod', 'Admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked from server')
    message = f"You have been kicked from {ctx.guild.name} for {reason}"
    await member.send(message)


# Banning someone
# bans a user with a reason
@client.command()
@commands.has_any_role('Mod', 'Admin')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f"@{member} is banned!")
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)

# Unabnning command 
@client.command()
@commands.has_any_role('Mod', 'Admin')
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
    #if name match, then we will unban user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f' User {user.mention} has been unbanned')
      return 
'''
# cogs help organize code 
@client.command()
async def load(ctx, extension): #loading cog
  client.load_extension(f'cogs.{extension}')
  await ctx.send("cogs loaded")

@client.command()
async def unload(ctx, extension): #unloading cog
  client.unload_extension(f'cogs.{extension}')
  await ctx.send("cogs unloaded")
 
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
'''
#use bot token----code that links bot to application(master key)
client.run('ODIxNjU0MzQ5OTYwODM5MjA5.YFG3Pg.KH5HwwiHaoD6FWg9p4xWuIIouME')

