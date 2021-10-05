import os
import discord
import requests
from discord.ext import commands

class PiNumber(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pi command is ready")

    @commands.command(help='Lấy n chữ số pi')
    async def pi(self, ctx, *, n_digits: int = 300):
        if n_digits < 1:
            await ctx.send("Số chữ số của `π` phải lớn hơn `0`")
            return
        elif n_digits > 4000:
            await ctx.send("Không thể hiện thị quá `4000` chữ số `π`")
            return
        n_digits -= 1
        
        pi = '3'
        count = 0
        max_digit = 1000

        if n_digits > 1:
            pi += '.'

        while count * max_digit < n_digits:
            fetch_digit = min(n_digits - count * max_digit, max_digit)
            pi += fetch_pi(count * max_digit + 1, fetch_digit)

            count += 1

        embed = discord.Embed(
            title=f'{n_digits+1} chữ số của π:',
            description=pi,
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)

def fetch_pi(start, n_digits):
    url = f'http://api.pi.delivery/v1/pi?start={start}&numberOfDigits={n_digits}'
    res = requests.get(url=url)
    data = res.json()
    return data['content']

def setup(client):
    client.add_cog(PiNumber(client))
