import requests
import discord
from discord.ext import commands

class Sequence(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sequence command is ready')

    @commands.command(aliases=['seq'], help='Tìm kiếm dãy số nguyên khớp nhất với input')
    async def sequence(self, ctx, *, numbers: str):
        numbers = numbers.split(' ')
        try:
            for i in range(len(numbers)):
                numbers[i] = int(numbers[i])

        except ValueError:
            await ctx.send('Dãy số chỉ được chứa số nguyên thôi :rolling_eyes:')
            return

        data = fetch_oeis(numbers)
        if data == None:
            await ctx.send('Không thể tìm thấy dãy số trùng khớp nào :cry:')

        description = ''
        for ind, seq in enumerate(data[:5]):
            link = f"http://oeis.org/{formatSeqID(seq['number'])}"
            description += f"**[{ind+1}. {seq['name']}]({link})**\n"
            description += limitSequence(seq['data'], 20) + '\n\n'

        embed = discord.Embed(
            title='Những dãy số nguyên khớp nhất',
            description=description,
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)
        
def fetch_oeis(nums):
    format_seq = ','.join([str(n) for n in nums])
    url = f'https://oeis.org/search?fmt=json&start=0&q={format_seq}'
    res = requests.get(url=url)
    data = res.json()
    return data['results']

def limitSequence(seq, limit):
    return ', '.join(seq.split(',')[:limit]) + ',...'

def formatSeqID(id: int):
    return f"A{str(id).rjust(6, '0')}"

def setup(client):
    client.add_cog(Sequence(client))
