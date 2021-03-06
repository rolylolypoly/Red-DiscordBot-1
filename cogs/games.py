import discord
import json
import inspect
import os
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks

class GameRanks:
    """Allows users to recieve select roles on command."""

    def __init__(self, bot):
        self.bot = bot
        try:
            self.games = dataIO.load_json('data/games/games.json')
        except FileNotFoundError:
            self.games = {}

    def write_json(self):
        filename = 'data/games/games.json'
        dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            os.mkdir(dir)
        dataIO.save_json(filename, self.games)

    @commands.command(pass_context=True)
    async def gamedebug(self, ctx):
        server = ctx.message.server
        #await self.bot.say(ctx.message.author.mention)
        for key,val in inspect.getmembers(list(server.members)[0]):
        #for member in list(server.members):
            await self.bot.say(str(key) + ': ' + str(type(val)))

    @commands.command(pass_context=True)
    async def game(self, ctx, role : discord.Role):
        """Allows a user to add themselves to a rank."""
        server = ctx.message.server
        if not server.id in self.games or not role.id in self.games[server.id]:
            await self.bot.say('The requested role is not available as a game')
        else:
            await self.bot.say(str(len(ctx.message.author.roles)))
            ctx.message.author.roles.append(role)
            await self.bot.say(str(len(ctx.message.author.roles)))
            await self.bot.say('Role added')

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def addgame(self, ctx, role : discord.Role):
        """Administration of joinable ranks."""
        server = ctx.message.server
        if not server.id in self.games:
            self.games[server.id] = []
        self.games[server.id].append(role.id)
        self.write_json()

def setup(bot):
    bot.add_cog(GameRanks(bot))
