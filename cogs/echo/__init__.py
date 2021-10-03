import os
import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')

class Echo(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, member: discord.Member):

        welcome_channel = self.client.get_channel(int(WELCOME_CHANNEL_ID))
        await welcome_channel.send('hello')

        await ctx.send(member.name)
        await ctx.send(member.display_name)
        

def setup(client):
    client.add_cog(Echo(client))
