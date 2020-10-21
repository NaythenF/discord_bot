import discord
import discord.ext.commands as commands
import random
import queue as q

class oh_queue(commands.Cog):
    def __init__(self):
        self.queue = None
        self.lst = None
        self.mae_helping = '\u200b'
        self.naythen_helping = '\u200b'
        self.disp = None
        self.msg = None
        self.started = False

    @commands.command()
    async def start(self, ctx):
        await ctx.message.delete()
        self.started = True
        self.queue = q.Queue()
        self.lst = list()
        self.disp = discord.Embed(color=discord.Colour.blue())
        self.disp.add_field(name='CS 211 OH Queue', value='\u200b', inline=False)
        self.disp.add_field(name='Currently waiting:', value='\u200b', inline=False)
        self.disp.add_field(name='Naythen is helping:', value='\u200b', inline=False)
        self.disp.add_field(name='Mae is helping:', value='\u200b', inline=False)
        self.msg = await ctx.send('Welcome to CS211 OH!', embed=self.disp)

    @commands.command()
    async def qme(self, ctx):
        if self.started:
            if ctx.message.author.nick not in self.lst and self.naythen_helping != ctx.author.name.nick and self.mae_helping != ctx.author.name.nick:
                self.queue.put_nowait(ctx.message.author.nick)
                self.lst.append(ctx.message.author.nick)
                await self.update()
        await ctx.message.delete()

    @commands.command()
    async def get(self, ctx):
        if self.started:
            if ctx.author.name == 'Naythen':
                if not self.queue.empty():
                    removed = self.queue.get_nowait()
                    self.naythen_helping = removed
                    self.lst.remove(removed)
                else:
                    self.naythen_helping = '\u200b'
            elif ctx.author.name == 'Mae Mastin':
                if not self.queue.empty():
                    removed = self.queue.get_nowait()
                    self.mae_helping = removed
                    self.lst.remove(removed)
                else:
                    self.mae_helping = '\u200b'
            await self.update()
            await ctx.message.delete()

    async def update(self):
        p = '\u200b'.join(self.lst)
        self.disp.set_field_at(index=1, name='Currently waiting:', value=p if p else '\u200b', inline=False)
        self.disp.set_field_at(index=2, name='Naythen is helping:', value=self.naythen_helping, inline=False)
        self.disp.set_field_at(index=3, name='Mae is helping:', value=self.mae_helping, inline=False)
        await self.msg.edit(embed=self.disp)





