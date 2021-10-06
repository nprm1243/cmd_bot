import os
import discord
from discord.ext import commands
#set up translate
import googletrans
from googletrans import Translator

class Sample(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command(help="+ ngôn ngữ muốn dịch đến(vi/en) + 'Từ / câu cần dịch'")
    async def translate(self, ctx, req: str = "en", *, message: str = None):
        if message == None:
            await ctx.send("Missing Text translate!")
        else:
            await ctx.send(f"{trans(message, language_req=req)}")

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

def setup(client):
    client.add_cog(Sample(client))