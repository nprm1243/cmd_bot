import os
import discord
import requests
import lxml
from bs4 import BeautifulSoup
from discord.colour import Color
import bs4
from discord.ext import commands
from urllib.parse import urlparse

class Docs_searcher(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Docs_searcher commands is ready")

    @commands.command()
    async def docs(self, ctx, *, req: str):
        tmp = docs_searching(req, 'nol')
        embed = discord.Embed(
            title = 'Docs searching bot',
            color = discord.Color.orange()
        )
        if (len(tmp) == 0):
            embed.add_field(
                name = 'can\'t found document!',
                value = 'sorry :(',
                inline = False
            )
            await ctx.send(embed = embed)
        else:
            for link in tmp:
                _link = link[0]
                _title = link[1]
                embed.add_field(
                    name =  f'{_title}',
                    value = f'[click here]({_link})',
                    inline = False
                )
            await ctx.send(embed = embed)
                

def docs_searching(docs_req, type):

    # ====== PREPARE VARIABLE ======
    url = 'empty'

    # ====== PROCESSING ======
    if (type == 'nol'):
        url =  'https://www.google.com/search?q=typefile%3Apdf+' + docs_req + '&rlz='

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('a')

    res = []

    i = 0

    for link in links:
        try:
            if ('.pdf' in link.get('href', []) or '/pdf' in link.get('href', []) ):
                print('yay')
                _link = link.get('href', [])
                title = ""
                try:
                    req = requests.get(str(link.get('href', [])))
                    _soup = BeautifulSoup(req.text, "lxml")
                    try:
                        title = str(_soup.title.string)
                    except Exception as e:
                        title = 'don\'t know'
                except Exception as e:
                    idx = _link.find('.pdf')
                    _link = _link[7:idx+4]
                    if (is_link_valid(_link)):
                        print(_link)
                        #req = requests.get(_link)
                        #_soup = BeautifulSoup(req.text, "lxml")                            
                        title = 'don\'t know'
                    else:
                        continue
                #hihi.append(str(f"```{title} : {link.get('href', [])}```"))
                if (title == 'don\'t know'):
                    st = str(_link)
                    st = st.split('/')
                    title = st[-1] + '(' + st[2] + ')'
                print(title)
                tmp = []
                tmp.append(_link)
                tmp.append(title)
                res.append(tmp)
                print(f"```{title} : {link.get('href', [])}```")
                #huhu = huhu + str(f"{title} \n {link.get('href', [])}") + '\n'
                i = i+1
            if (i == 5):
                break
        except Exception as e:
            pass

    return res

def is_link_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def setup(client):
    client.add_cog(Docs_searcher(client))