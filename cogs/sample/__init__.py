import os
import discord
from discord.ext import commands

class Sample(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    # Khi lệnh được tạo ra thì sẽ chạy hàm này đầu tiên
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # Định nghĩa lệnh "sample_cmd"
    @commands.command()
    async def sample_cmd(self, ctx, *, text: str):
        pass

    # Định nghĩa lệnh "sample_cmd2"
    @commands.command()
    async def sample_cmd2(self, ctx, code: int = None, *, text: str = None):
        pass

def setup(client):
    client.add_cog(Sample(client))
