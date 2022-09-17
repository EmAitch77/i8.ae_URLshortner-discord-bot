from i8 import i8
from dotenv import load_dotenv, find_dotenv
import os
import json
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

load_dotenv(find_dotenv())
token= os.getenv('TOKEN') # Bot Token
def get_server_id():
    f= open('config.json', 'r')
    j= json.load(f)
    return j['server_id']
serverid= "1020044841922609313"
bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
api_key = os.getenv("I8") # Your i8.ae API Key
api     = i8(api_key=api_key)

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild= discord.Object(id=int(serverid)))
        self.synced = True
        print(f"Bot is online as {bot.user.display_name}")
        activity = discord.Game(name= f"With URLs", type=3)
        await bot.change_presence(status=discord.Status.idle, activity=activity)
bot = abot()
tree= app_commands.CommandTree(bot)


@tree.command(name="ping", description="Bot latency", guild=discord.Object(id=int(serverid)))
async def self(interation: discord.Interaction):
    await interation.response.send_message(f"Pong!! **latency: `{round(bot.latency * 1000)}ms` <:AstolfoTea:996714601465008169>**")


@tree.command(name="short", description="Shorten a URL", guild=discord.Object(id=int(serverid)))
async def self(interation: discord.Interaction, url:str, password: Optional[str]):
    if 'http://' in url:
        embed = discord.Embed(
                title="Error: http links are banned cuz of security purposes !",
                color= discord.Colour.red()
            )
        embed.set_author(name=f"{bot.user.display_name} Bot", icon_url=bot.user.display_avatar)
        embed.set_footer(text=f"{bot.user.display_name} | Developed By: Moemen Hamdy", icon_url=None)
        await interation.response.send_message(embed=embed, ephemeral=True)
    elif 'https://' in url:
        shorten_url = None
        try:
            shorten_url = api.short(url=url, password=password)
        except:
            embed = discord.Embed(
                    title="Error: Unable to short this url !",
                    color= discord.Colour.red()
                )
            embed.set_author(name=f"{bot.user.display_name} Bot", icon_url=bot.user.display_avatar)
            embed.set_footer(text=f"{bot.user.display_name} | Developed By: Moemen Hamdy", icon_url=None)
            await interation.response.send_message(embed=embed, ephemeral=True)
            return
        if password == None:
            dsc  = f"**Shorten URL:** {shorten_url}\n\n"
            rpl  = f"**Shorten Url is:** {shorten_url} <:AstolfoTea:996714601465008169>"
            eph  = False
        else:
            dsc  = f"**Shorten URL:** {shorten_url}\n**password:** || {password} ||\n"
            rpl  = f"**Shorten Url is:** {shorten_url} <:AstolfoTea:996714601465008169> \n**password:** || {password} || <:Serfmoderator:996714611044786246> "
            eph  = True
        embed = discord.Embed(
            title= f"Shorten url for: `{url}`",
            description= dsc,
            #url= shorten_url,
            color= discord.Colour.random()
            )
        qr_img = f"{shorten_url}/qr"
        embed.set_thumbnail(url=qr_img)
        embed.set_author(name=f"{bot.user.display_name} Bot", icon_url=bot.user.display_avatar)
        embed.set_footer(text=f"{bot.user.display_name} | Developed By: Moemen Hamdy", icon_url=None)
        await interation.response.send_message(content=rpl, embed=embed,ephemeral=eph)
    else:
        embed = discord.Embed(
                title="Error: Please enter a valid URL !",
                color= discord.Colour.red()
            )
        embed.set_author(name=f"{bot.user.display_name} Bot", icon_url=bot.user.display_avatar)
        embed.set_footer(text=f"{bot.user.display_name} | Developed By: Moemen Hamdy", icon_url=None)
        await interation.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    bot.run(token)
