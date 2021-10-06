#set up bot
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import nest_asyncio
nest_asyncio.apply()

#set up parse
from bs4 import BeautifulSoup
import urllib.request

#set up translate
import googletrans
from googletrans import Translator

load_dotenv()
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

class Get_books(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command(help="+ sách muốn lấy ")
    async def get_books(self,ctx,*,message:str=None):
        if message == None:
            await ctx.send("Missing Book - key words")
        else:
            x = trans(message)
            if (message != self.client.user):
                await ctx.send(f"Ttrue , access request get '{x}' \n Wait me few seconds")
                n, book = get_url(link_to(x))
                if n >= 6:
                    for i in range(0, 5):
                        await ctx.send(book[i])
                elif (0 < n < 6):
                    for i in range(0, n):
                        await ctx.send(book[i])
                elif n == 0:
                    await ctx.send("Not found!")

def setup(client):
    client.add_cog(Get_books(client))

def link_to(x):
    x = x.replace(" ", "%20")
    search = f"https://vn1lib.org/s/{x}"
    return search

def trans(text,language_req:str="en"):
    translator = Translator()
    if (str(translator.detect(text).lang) == "vi"):
        a = translator.translate(text, src="vi")
        translated_text = a.__dict__()["text"]
        return translated_text
    elif (str(translator.detect(text).lang) == "en") and (language_req == "vi"):
        a = translator.translate(text,dest="vi")
        translated_text = a.__dict__()["text"]
        return translated_text
    else:
        return text

def get_url(url):
    '''
    :param url: web to fund book
    :return:  5 link thoả mong muốn của mình
    '''
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    urls = []
    book_urls = []
    for book in soup.find_all('div', class_="resItemBox resItemBoxBooks exactMatch"):
        urls = book.find('a', href=True)
        dem = book.find("div", {"class": "book-rating"}).get_text(strip=True)
        dem = dem[0:dem.find("/")]
        if 3.0 <= float(dem) <= 5.0:
            book_urls.append("https://vn1lib.org" + urls['href'])
    return len(book_urls), book_urls