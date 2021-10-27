import discord
import random
import datetime
from discord.ext import commands
from datetime import datetime
import math

class MatchPercent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Match command is ready")

    @commands.command(help='Đo độ hợp nhau của 2 người :>')
    async def howmatch(self, ctx: commands.Context, *mentions: discord.Member):

        print(len(mentions))

        if (len(mentions) == 2):
            firstPercent = randomPercent(mentions[0]) * randomPercent(mentions[1])
            randomSeed = firstPercent * 10 + 1
            random.seed(randomSeed)
            
            result = 1
            # Pytago

            a = random.random() % 100
            b = random.random() % 100
            pytago = math.sqrt(a**2 + b**2)

            # Talet

            firstTriagle_a = 3
            firstTriagle_b = 4
            firstTriagle_c = 5
            secondTriagle_a = pytago
            secondTriagle_b = pytago/3 * 4
            secondTriagle_c = pytago/3 * 5

            # Magic

            firstPercent = firstPercent / 10**(int(math.log10(firstPercent)) + 1)
            secondPercent = secondTriagle_b / 10**(int(math.log10(secondTriagle_b)) + 1)
            thirdPercent = secondTriagle_c / 10**(int(math.log10(secondTriagle_c)) + 1)

            percent = 0


            if firstPercent + secondPercent > thirdPercent and secondPercent + thirdPercent > firstPercent and firstPercent + thirdPercent > secondPercent:
                # Heron

                p = (firstPercent + secondPercent + thirdPercent)/2
                percent = math.sqrt(p * (p - firstPercent) * (p - secondPercent) * (p - thirdPercent))

            step = 5
            while (percent < 0.01 and step > 0):
                percent = percent * 10
                step -= 1

            percent = min(1, percent*10)

            embed = discord.Embed(
                title="Đôi bạn có hợp nhau không ?",
                description=f'{str(round(percent*100, 0))} %' +('♥' if percent >= 0.5 else '😁'),
                color=discord.Color.orange(),
            )

            await  ctx.send(embed = embed)
        else:

            embed = discord.Embed(
                title="Đôi bạn có hợp nhau không ?",
                description='wrong input',
                color=discord.Color.orange(),
            )

            await  ctx.send(embed = embed)

def randomPercent(seed):
    today = datetime.today().strftime('%Y-%m-%d')
    seed = f'{seed}/{today}'
    rng = random.Random(seed)
    return rng.randint(0, 100)

def setup(client):
    client.add_cog(MatchPercent(client))
