import discord
import os

from error_handling import *
from support import *

intents = discord.Intents.all()
client = discord.Client(intents=intents)

support = ["blackhole-days", "technical-support", "project-subscription"]


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_guild_channel_create(channel):
  """ Run while a ticket channel is created """
#   command_options_bocal = """
# `1. !showtickets`
# Shows a log of the all of the tickets and its information

# `2. !get [blackhole/technical/subscription]`
# Shows the number of tickets of selected the category
#   """

#   embed1 = discord.Embed(
#       title="Available Commands: ",
#       color=0x55FF00,
#   )
#   embed1.add_field(
#       name="Format: ",
#       value=command_options_bocal,
#   )

  ticket_format = """
`1. Request for blackhole days`
Format:  `!add [intra-id] [blackhole-days] [absorption-date, format: DD-MM-YYYY]`
Example: `!add tsabre blackhole-days 21-09-21`

`2. Request for tech support`
Format:  `!add [intra-id] [technical-support] ["issue"]`
Example: `!add maiman-m technical-support "i cant connect to intra"`

`3. Request for a project subscription`
Format:  `!add [intra-id] [project-subscription] [project_name]`
Example: `!add rsoo project-subscription minishell`
"""
  embed2 = discord.Embed(
      title="Format: ",
      color=0x00FF55,
  )
  embed2.add_field(
      name="Options: ",
      value=ticket_format,
  )
  if channel.name.startswith('ticket-'):
    # await channel.send(embed=embed1)
    await channel.send(embed=embed2)


@client.event
# delete ticket from csv, or dictionary
async def on_guild_channel_delete(channel):
  """ Run while a channel is deleted """
  if channel.name.startswith('ticket-'):
    remove_closed_tickets(channel.name)


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.channel.name.startswith("ticket-checking"):
    if message.content.startswith("!delete"):
      guild = client.get_guild(1158255853518983198)
      channelName = message.content.split()[1]
      channel = discord.utils.get(guild.channels, name=channelName)
      if channel is not None:
        await channel.delete()
    if message.content.startswith("!get"):
      msg = message.content.split()
      if len(msg) == 1:
        await message.channel.send("get blackhole/technical/subscription")
        return
      field = get_csv_info_title(message.content.split()[1])
      if field is None:
        await message.channel.send(f"only {support} accepted")
        return
      num = get_csv_info_num(message.content.split()[1])
      info = get_csv_info_field(message.content.split()[1])
      embed = discord.Embed(
          title=f"{field}: opened support tickets",
          color=0x00FF00,
      )
      embed.add_field(name="\u200b", value=info)
      await message.channel.send(embed=embed)
    if message.content.startswith("!showtickets"):
      b_num = get_csv_info_num("blackhole")
      t_num = get_csv_info_num("technical")
      s_num = get_csv_info_num("subscription")
      embed = discord.Embed(
          title=f"all support tickets",
          color=0x00FF00,
      )
      embed.add_field(
          name="blackhole-days",
          value=b_num,
      )
      embed.add_field(
          name="technical-support",
          value=t_num,
      )
      embed.add_field(
          name="project-subscription",
          value=s_num,
      )
      await message.channel.send(embed=embed)
  if message.channel.name.startswith('ticket-'):
    if message.content.startswith("!add"):
      double_quote = re.compile(r'"(.+?)"', re.IGNORECASE)
      in_double_quote = double_quote.findall(message.content)
      msg = message.content.split()
      if msg[2] == support[0]:
        if validate_date(msg[3]) == 1:
          print(msg[3])
          dt = msg[3].split("-")[0]
          mnth = msg[3].split("-")[1]
          print(dt, mnth)
        else:
          await message.channel.send("is your absorption date in DD-MM-YY format?")
          return
      msg.remove("!add")
      if len(in_double_quote) == 0:
        store_support(msg, message)
        store_pending(msg, "a")
      else:
        new = []
        new.append(msg[0])
        new.append(msg[1])
        new.append(in_double_quote[0])
        store_support(new, message)
        store_pending(new, "a")

my_secret = os.environ['SLASH']
client.run(my_secret)
