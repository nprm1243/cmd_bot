import os
import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')

class Echo(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Echo command is ready")

    @commands.command(help="Nhại lại tin nhắn của người dùng")
    async def echo(self, ctx, *, message = ""):
        if message == "":
            await ctx.send('Phải nhắn gì thì mới nhại lại được chứ :expressionless:')
        else:
            await ctx.send(message)
        
def setup(client):
    client.add_cog(Echo(client))
