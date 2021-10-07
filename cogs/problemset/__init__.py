import os
import discord
from discord.colour import Color
import bs4
from discord.ext import commands
from cogs.problemset import searcher

COMMAND_LIST = [
    ['codeforces' , """
        + codeforces tags : Trả về tất cả các tag trong codeforces problemset
        + codeforces contest: Trả về contests sắp diễn ra trên codeforces
        + codeforces <rating> : Trả về 1 problem với rating tương đương
        + codeforces <tag> : Trả về 1 problem với tag tương đương
        + codeforces <min_rating> <max_rating> : Trả về 1 problem có rating nằm trong khoảng [min_rating, max_rating]
        + codeforces <tag> <rating> : Trả về 1 problem với tag và rating tương đương
        + codeforces <min_rating> <max_rating> <num> : Trả về num problem có rating nằm trong khoảng [min_rating, max_rating]
        + codeforces <tag> <min_rating> <max_rating> : Trả về 1 problem với tag trong khoảng [min_rating, max_rating]
        + codeforces <tag> <min_rating> <max_rating> <num>: Trả về num problem với tag trong khoảng [min_rating, max_rating]
    """],
    ['codechef' , """
        + codechef contest : Trả về contest sắp diễn ra trên codechef
        + codechef tags <value> : trả về tất cả tags có số lượng bài tập >= 10 (tags: difficulty, topics)
        + codechef <tag> : Trả về 1 problem với tag tương đương
        + codechef <tag> <num> : Trả về num problem với tag tương đương
    """], 
    ['hackerrank' , """
        + hackerrank skills : trả về các skill hỗ trợ trong hackerrank
        + hackerrank <skill> tags : trả về các tags có trong skill trên hackerrank
        + hackerrank <skill> <tag_1> <tag_2> ... <tag_n> <num> : tìm kiếm bài tập theo skill trên hackerrank dựa trên các tags (thứ tự của tags không quan trọng, num là số lượng bài cần tìm)
    """],
    ['we will add more features', """
        + Nhiều điều thú vị nữa sẽ tiếp tục được cập nhật trong tương lai^^
    """]    
]

THUMB_URL = {
    'codeforces' : 'https://cdn.discordapp.com/attachments/893738488137142286/895216466192896060/EkSlLWf2-04k5Y5F_MDLqoXPdo0TyZX3zKdCfsEUDqVB7INUypTOd6AVmkE_X7ej3JuR.png',
    'hackerrank' : 'https://cdn.discordapp.com/attachments/893738488137142286/895213908753801246/HackerRank_Icon-1000px.png',
    'codechef' : 'https://cdn.discordapp.com/attachments/893738488137142286/895217645530513418/ce4fd2180646452aa0b03c3ffa3ef8e2.png'
}

BANNER_URL = {
    'codeforces' : 'https://cdn.discordapp.com/attachments/893738488137142286/895291549397704704/Blue_and_Purple_Casual_Corporate_App_Development_Startup_Brand_Guidelines_Presentation.png'
}

class problemset(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Problemset commands is ready")

    @commands.command(help = 'trợ giúp cho các câu lệnh codeforces, codechef và hackerrank')
    async def codehelp(self, ctx):
        embed = discord.Embed(
            title = 'codehelp',
            color = discord.Color.orange()
        )
        for item in COMMAND_LIST:
            embed.add_field(
                name = f'{item[0]}',
                value = f'{item[1]}',
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(help = 'lấy random bài trên codeforces dựa vào tag, và rating')
    async def codeforces(self, ctx, *args):
        tag = ''
        mn = 600
        mx = 3600
        num = 1
        if (len(args) == 1):
            if (args[0].isnumeric()):
                mn = mx = args[0]
            elif (args[0] == 'tags'):
                embed = discord.Embed(
                    title = 'codeforces tags',
                    description =searcher.get_link.cf_tags(),
                    color = discord.Color.red()
                )
                embed.set_thumbnail(url = THUMB_URL['codeforces'])
                embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed = embed)
                return 0
            elif (args[0] == 'contest'):
                res = searcher.get_contest.codeforces_contest()
                embed = discord.Embed(
                    title = 'codeforces comming contest',
                    color = discord.Color.red()
                )
                embed.set_thumbnail(url = THUMB_URL['codeforces'])
                embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
                embed.set_image(url = BANNER_URL['codeforces'])
                for item in res:
                    embed.add_field(
                        name = f'{item[0]}',
                        value = f"""
                            `{item[2]} | `[`Registration for the contest`]({item[1]})
                        """,
                        inline=False
                    )
                await ctx.send(embed=embed)
                return 0
            else:
                tag = args[0]
        elif (len(args) == 2):
            if (args[0].isnumeric()):
                mn = args[0]
                mx = args[1]
            else:
                tag = args[0]
                mn = mx = args[1]
        elif (len(args) == 3):
            if (args[0].isnumeric()):
                mn = args[0]
                mx = args[1]
                num = int(args[2])
            else:
                tag = args[0]
                mn = args[1]
                mx = args[2]
        else:
            tag = args[0]
            mn = args[1]
            mx = args[2]
            num = int(args[3])
        res = searcher.get_link.cf_searching_problem(tag, mn, mx, num)
        embed = discord.Embed(
            title = 'codeforces',
            color = discord.Color.red()
        )
        embed.set_thumbnail(url = THUMB_URL['codeforces'])
        embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
        for item in res:
            embed.add_field(
                name = f'{item[1]}',
                value = f'[click here]({item[0]})',
                inline = False
            )
        await ctx.send(embed=embed)

    @commands.command(help = 'lấy random bài trên codechef dựa vào tag')
    async def codechef(self, ctx, *args):
        tag = ''
        num = 1
        if (len(args) == 1):
            tag = args[0]
            num = 1
            if (tag == 'contest'):
                res = searcher.get_contest.codechef_contest()
                embed = discord.Embed(
                    title = 'codechef comming contest',
                    value = f'[contest page](res[1])',
                    color = discord.Color.red()
                )
                embed.set_thumbnail(url = THUMB_URL['codechef'])
                embed.set_image(url = res[0])
                embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
                embed.add_field(
                    name = f'{res[2]}',
                    value = f'contest page: {(res[1])}',
                    inline=False
                )
                await ctx.send(embed=embed)
                return 0

        else:
            tag = args[0]
            if (tag == 'tags'):
                type = args[1]
                embed = discord.Embed(
                    title = 'codechef tags',
                    description =searcher.get_link.cc_tags(type),
                    color = discord.Color.red()
                )
                embed.set_thumbnail(url = THUMB_URL['codechef'])
                embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed = embed)
                return 0
            else:
                num = int(args[1])
        res = searcher.get_link.cc_searching_problem(tag, num)
        embed = discord.Embed(
            title = 'codechef',
            color = discord.Color.light_gray()
        )
        embed.set_thumbnail(url = THUMB_URL['codechef'])
        embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
        for item in res:
            embed.add_field(
                name = f'{item[0]}',
                value = f'[click here]({item[1]})',
                inline = False
            )
        await ctx.send(embed=embed)

    @commands.command(help = 'lấy random bài trên hackerrank dựa vào skill và tags')
    async def hackerrank(self, ctx, *args):
        skill = ''
        status = []
        skills = []
        difficulty = []
        subdomains = []
        num = 1
        skill = args[0]
        if (args[0] == 'skills'):
            embed = discord.Embed(
                title = 'hankerrank skills',
                description = str(searcher.get_link.hr_skills()),
                color = discord.Color.red()
            )
            embed.set_thumbnail(url = THUMB_URL['hackerrank'])
            embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return 0
        if (len(args) > 1):
            if (args[1] == 'tags'):
                embed = discord.Embed(
                    title = 'hankerrank skills',
                    color = discord.Color.red(),
                )
                embed.set_thumbnail(url = THUMB_URL['hackerrank'])
                embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
                res = searcher.get_link.hr_tags(args[0])
                embed.add_field(
                    name = 'status',
                    value = res['status'],
                    inline = False
                )
                embed.add_field(
                    name = 'skills',
                    value = res['skills'],
                    inline = False
                )
                embed.add_field(
                    name = 'difficulty',
                    value = res['difficulty'],
                    inline = False
                )
                embed.add_field(
                    name = 'subdomains',
                    value = res['subdomains'],
                    inline = False
                )
                await ctx.send(embed=embed)
                return 0
        for i in range(1, len(args)):
            st = str(args[i])
            st = st.replace('+', ' ')
            if ('solved' in st):
                status.append(st)
            elif ('(' in st):
                skills.append(st)
            elif ('easy' in st or 'medium' in st or 'hard' in st):
                difficulty.append(st)
            elif (not st.isdigit()):
                subdomains.append(st)
            else:
                num = int(st)
        res = searcher.get_link.hr_searching_problem(skill, status, skills, difficulty, subdomains, num)
        embed = discord.Embed(
            title = 'hackerrank',
            color = discord.Color.red()
        )
        embed.set_thumbnail(url = THUMB_URL['hackerrank'])
        embed.set_author(name = 'Request by ' + str(ctx.message.author)[:-5], icon_url=ctx.message.author.avatar_url)
        for item in res:
            embed.add_field(
                name = f'{item[0]}',
                value = f'[click here]({item[1]})',
                inline = False
            )
        await ctx.send(embed=embed)




# setup cog
def setup(client):
    client.add_cog(problemset(client))