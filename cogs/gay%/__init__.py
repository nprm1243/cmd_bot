import discord
import random
from discord.ext import commands
from datetime import datetime

class GayPercent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Gay command is ready")

    @commands.command(aliases=['gay%'])
    async def howgay(self, ctx: commands.Context, *members: discord.Member):
        description = []

        for member in members:
            percent = randomPercent(member)
            description.append(f'**{member.display_name}** có {percent}% tỉ lệ gay')

        embed = discord.Embed(
            title="🏳️‍🌈 Bạn có thẳng như mình nghĩ?",
            description='\n'.join(description),
            color=discord.Color.orange(),
        )

        if len(description) == 0:
            percent = randomPercent(ctx.author)
            flag = '🏳️‍🌈' if percent > 25 else '🏳️'
            await ctx.send(f'{flag} Bạn có {percent}% tỉ lệ gay')
        else:
            await ctx.send(embed=embed)

def randomPercent(seed):
    today = datetime.today().strftime('%Y-%m-%d')
    seed = f'{seed}/{today}'
    rng = random.Random(seed)
    return rng.randint(0, 100)

def setup(client):
    client.add_cog(GayPercent(client))
