import os
import discord
from discord.ext import commands

class Sample(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # run when command is ready
        print("Sample command is ready")

        # send to specific channel
        # WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')
        # self.channel = self.client.get_channel(int(WELCOME_CHANNEL_ID))
        # await self.channel.send("Welcome, I'm back")

    @commands.command()
    async def sample_cmd(self, ctx, *, text: str):
        # handle "sample_cmd" command, with "text" parameter
        pass
        # send simple message:
        # await ctx.send("something")

    @commands.command()
    async def sample_cmd2(self, ctx, code: int = None, *, text: str = None):
        # handle "sample_cmd2" command, with "code" (integer) and "text" (string) parameters
        if code == None:
            print("code parameter is missing")
        elif text == None:
            print("text parameter is missing")
        else:
            pass

def setup(client):
    client.add_cog(Sample(client))
