import discord.ext.commands as cmd
import random

class hangman(cmd.Cog):
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

    @cmd.command()
    async def hm(self, ctx):
        if not self.game_in_progress:
            self.game_in_progress = True
            self.word = random.choice(self.dict).rstrip()
            self.real_word = ['_' for i in range(len(self.word))]
            await ctx.send(f'{ctx.author.name} has just started a game of hangman!\nUse `$guess <letter>` to guess.')
            await self.display(ctx)
        else:
            await ctx.send('A game of hangman is already in progress!')

    @cmd.command()
    async def guess(self, ctx, letter: str):
        letter = letter.lower()
        await ctx.send(f"You have guessed {letter}!")
        if self.game_in_progress:
            if len(letter) > 1:
                await ctx.send('Your guess must be 1 character!')
            elif letter not in self.guessed:
                self.guessed.add(letter)
                if letter in self.word:
                    await ctx.send('Good guess!')
                    for i in range(len(self.word)):
                        if self.word[i:i+1] == letter:
                            self.real_word[i] = letter
                else:
                    await ctx.send('Bad guess...')
                    self.stage = str(int(self.stage) + 1)
            else:
                await ctx.send('You have already guessed that!')
            potential_win = ''.join(self.real_word)
            if potential_win == self.word:
                await self.winner(ctx)
            elif self.stage == '7':
                await self.murderer(ctx)
            else:
                await self.display(ctx)

    @cmd.command()
    async def end(self, ctx):
        if self.game_in_progress:
            await ctx.send(f'You have decided to end the game early. The word was: {self.word}.')
            self.cleanup()
        else:
            await ctx.send('A game is not currently in progress.')

    async def winner(self, ctx):
        path = 'stages/winner.txt'
        f = open(path)
        stg = ''
        for line in f.readlines():
            stg += f'{line}'
        f.close()
        wrd = ''.join([let + ' ' for let in self.word])
        await ctx.send(f'```{stg}\n {wrd}\n Congratulations, you guessed the word!```')
        self.cleanup()

    async def murderer(self, ctx):
        path = 'stages/dead.txt'
        f = open(path)
        stg = ''
        for line in f.readlines():
            stg += f'{line}'
        f.close()
        wrd = ''.join([let + ' ' for let in self.real_word])
        await ctx.send(f'```{stg}\n {wrd}\n You lost! The word was: {self.word}.```')
        self.cleanup()

    async def display(self, ctx):
        path = 'stages/stage' + self.stage + '.txt'
        f = open(path)
        stg = ''
        for line in f.readlines():
            stg += f'{line}'
        f.close()
        wrd = ''.join([let+' ' for let in self.real_word])
        guessed = ''.join([let+' ' for let in self.guessed])
        await ctx.send(f'```{stg}\n {wrd}\n Guessed: {guessed}```')

    def cleanup(self):
        self.game_in_progress = False
        self.stage = '1'
        self.guessed = set()
        self.real_word = []
        return
