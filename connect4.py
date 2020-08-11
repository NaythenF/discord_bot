import discord
import discord.ext.commands as cmd
from enum import Enum

class Player(Enum):
    blue = 1
    red = 2
    neither = 3

class connect4(cmd.Cog):
    def __init__(self, bot, guild, size):
        self.bot = bot
        self.guild = guild
        self.size = size
        self.p1 = None
        self.p2 = None
        self.game_in_progress = False
        self.board = [[Player.neither for j in range(self.size)] for i in range(self.size)]
        self.bottoms = [0 for j in range(self.size)]



    @cmd.command()
    async def c4(self, ctx, name):
        if not self.game_in_progress:
            members = [member.name for member in discord.utils.get(self.bot.guilds, name=self.guild).members]
            if name[1:] not in members:
                await ctx.send(f'Sorry, {ctx.author.name}. I can\'t seem to find the person you want to play with.')
                return
            self.game_in_progress = True
            self.p1 = ctx.author.name
            self.p2 = name
            self.turn = self.p1
            await ctx.send(
                f'{ctx.author.name} has just started a game of Connect4 with {name}!\nUse $play <col> to play!')
            await self.display(ctx)
        else:
            await ctx.send('A game of Connect4 is already in progress!')


