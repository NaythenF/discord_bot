import os
import random
import discord
import old_hangman as hang
from dotenv import load_dotenv
from discord.ext import commands

# environment setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# command prefix
bot = commands.Bot(command_prefix='$')
# add cogs
bot.add_cog(hang.hangman(bot, "dictionary.txt"))
# ------------------------------------ #
# EVENTS                               #
# ------------------------------------ #
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user.name} has connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, we hope you enjoy your stay!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user.name:
        return

    if message.content == 'YEP':
        await message.add_reaction('🍆')
    elif message.content == 'Nathan is gay.':
        await message.channel.send('Of course he is!')
    elif message.content == 'Wait, how did you know that?':
        await message.channel.send('Everyone knows that kid likes to suck fat weiners.')

    await bot.process_commands(message)
# ------------------------------------ #
#                                      #
# ------------------------------------ #

# ------------------------------------ #
# COMMANDS                             #
# ------------------------------------ #
@bot.command(name = '99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the **100** emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name = 'choose-for-me', help='Given a selection of input choices, generates a random choice.')
async def choose_for_me(ctx, *choices : str):
    choices = list(map(str.strip, ''.join([string + ' ' for string in choices]).split(',')))
    out = '\n'.join(choices)
    await ctx.send(f'**Choices were:**\n{out}\n**I chose:**\n{random.choice(choices)}')

@bot.command(name='create-channel')
@commands.has_role('administrator')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
# ------------------------------------ #
#                                      #
# ------------------------------------ #

# ------------------------------------ #
# ERROR HANDLING                       #
# ------------------------------------ #
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:                
            print("exception not handled")
# ------------------------------------ #
#                                      #
# ------------------------------------ #

# run this bad boy
bot.run(TOKEN)
