import discord
import discord.ext.commands as commands
class Hangman(commands.Cog):
    def __init__(self, bot, path_to_dict):
        self.bot = bot
        self.game_in_progress = False
        self.player = None
        self.word = None
        f = open(path_to_dict, 'r')
        self.dict = f.readlines()
        f.close()
        self.stage = '1'
        self.guessed = set()
        self.real_word = []
        self.disp = discord.Embed(color=discord.Colour.green())
        self.msg = None
        self.authormsg = None
        self.botmsg = None
        self.win = False
        self.player = None

    @commands.command()
    async def hm(self, ctx):
        if not self.game_in_progress:
            await ctx.message.delete()
            self.player = ctx.message.author
            self.game_in_progress = True
            self.word = random.choice(self.dict).rstrip()
            self.real_word = ['_' for i in range(len(self.word))]
            await self.display(ctx)
        else:
            await self.clear_msg()
            self.authormsg = ctx.message
            self.botmsg = await ctx.send('A game of hangman is already in progress!')

    @commands.command()
    async def guess(self, ctx, letter: str):
        letter = letter.lower()
        if self.game_in_progress and self.player == ctx.message.author:
            await self.clear_msg()
            self.authormsg = ctx.message
            if len(letter) > 1:
                self.bot_msg = await ctx.send('Your guess must be 1 character!')
            elif letter not in self.guessed:
                self.guessed.add(letter)
                if letter in self.word:
                    self.botmsg = await ctx.send('Good guess!')
                    for i in range(len(self.word)):
                        if self.word[i:i+1] == letter:
                            self.real_word[i] = letter
                else:
                    self.botmsg = await ctx.send('Bad guess...')
                    self.stage = str(int(self.stage) + 1)
            else:
                self.botmsg = await ctx.send('You have already guessed that!')
            potential_win = ''.join(self.real_word)
            if potential_win == self.word:
                self.win = True
            await self.display(ctx)

    @commands.command()
    async def end(self, ctx):
        await self.clear_msg()
        if self.game_in_progress and self.player == ctx.message.author:
            await ctx.send(f'You have decided to end the game early. The word was: {self.word}.')
            self.cleanup()
        else:
            await ctx.send('A game is not currently in progress.')

    async def clear_msg(self):
        if self.authormsg and self.botmsg is not None:
            await self.authormsg.delete()
            await self.botmsg.delete()

    def cleanup(self):
        self.game_in_progress = False
        self.stage = '1'
        self.guessed = set()
        self.real_word = []
        self.msg = None
        self.authormsg = None
        self.botmsg = None
        self.player = None
        self.disp = discord.Embed(color=discord.Colour.green())
        self.win = False
        return

    async def display(self, ctx):
        if self.win:
            path = 'stages/winner.txt'
        else:
            path = 'stages/stage' + self.stage + '.txt'
        f = open(path)
        print = '```'
        for line in f.readlines():
            print += f'{line}'
        print += '```'
        f.close()
        wrd = '``` ' + ''.join([let+' ' for let in self.real_word]) + '```'
        guessed = 'Guessed: ' + ''.join([let+' ' for let in self.guessed])
        if self.msg is None:
            self.disp.add_field(name='Hangman', value=print)
            self.disp.add_field(name='Word to Guess', value=wrd, inline=False)
            self.disp.add_field(name='Letters Guessed', value=guessed,
                                inline=False)
            self.msg = await ctx.send('Use `-guess <letter>` to guess.', embed=self.disp)
        else:
            self.disp.set_field_at(index=0, name='Hangman', value=print)
            self.disp.set_field_at(index=1, name='Word to Guess', value=wrd,
                                   inline=False)
            self.disp.set_field_at(index=2, name='Letters Guessed', value=guessed,
                                   inline=False)
            await self.msg.edit(embed=self.disp)
        if self.win:
            await self.clear_msg()
            await ctx.send("Congratulations, you guessed the word!")
            self.cleanup()
        if self.stage == '7':
            await self.clear_msg()
            await ctx.send(f"You lost! The word was: {self.word}")
            self.cleanup()