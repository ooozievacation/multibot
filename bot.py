# Import all the nessecary packages

from dotenv import load_dotenv
import discord, os, pybalt, yaml, aiofiles, base64
import random
from discord.ext import commands

# Specified list for working websites using pybalt

pybaltURLs = ["youtube.com","youtu.be","instagram.com","tiktok.com","twitter.com","x.com"]

# Loads the .env file and the data inside of it

load_dotenv(".env")
botToken = os.getenv("TOKEN")
botPrefix = os.getenv("PREFIX")
botStatusType = os.getenv("STATUS_TYPE").lower()
botStatusName = os.getenv("STATUS_NAME")
botStatusURL = os.getenv("STATUS_URL")
bot = commands.Bot(command_prefix=botPrefix,intents=discord.Intents.all())

# Function used for the custom Bot status
async def setStatus(statusType, statusName, statusURL):
    if statusType == "streaming":
        await bot.change_presence(activity=discord.Streaming(name=f"Streaming {statusName}", url=statusURL))
    elif statusType == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Listening to {statusName}"))
    elif statusType == "playing":
        await bot.change_presence(activity=discord.Game(name=f"Playing {statusName}"))
    elif statusType == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Watching {statusName}"))
    else:
        print("[!] The status type entry you entered is incorrect or unwritten.")

# Using on_ready() so if the bot runs the user knows its running

@bot.event
async def on_ready():
    await setStatus(botStatusType,botStatusName,botStatusURL)
    print(f"[!] {bot.user} has woke up from the multibot grave!")

# The specified commands for the bot

@bot.command(name="ping",description="Used to check the bot's ping to Discord")
async def ping(ctx):
    await ctx.send(f"Ping: {int(round(bot.latency*1000,0))}ms")

@bot.command(name="random",description="Chooses a random from a range")
async def ran(ctx, first:int, last:int):
    await ctx.send(f"From {first} to {last}, I choose {random.randint(first,last)}!")

@bot.command(name="download",description="Downloads a video")
async def download(ctx, url):
    guildUploadLimit = round(ctx.guild.filesize_limit/(1024*1024),2)
    for pybaltURL in pybaltURLs:
        if pybaltURL in url:
            dlPath = await pybalt.download(url, videoQuality='480')
            try:
                fileSize = round((os.path.getsize(dlPath)/(1024*1024)),2)
                if fileSize <= guildUploadLimit:
                    await ctx.send(f"-# video size: {fileSize} MB",file=discord.File(dlPath))
                else:
                    await ctx.send(f"Couldn't upload files bigger than {guildUploadLimit}MB! This will be implemented very soon by using Catbox.")
            finally:
                if dlPath and os.path.exists(dlPath):
                    os.remove(dlPath)
            return
    await ctx.send(f"Downloading files that aren't from these URLs `{' '.join(pybaltURLs)}` isn't implemented yet!")
    # DOWNLOADS FOR UNSUPPORTED URLS WILL BE IMPLEMENTED VERY SOON!!!

@bot.command(name="encodeb64",description=f"Encodes a string in Base64")
async def encodeb64(ctx, *, string):
    encoded = base64.b64encode(string.encode()).decode()
    await ctx.send(f"`{string}` encoded in Base64 is `{encoded}`.")

# Runs the bot with the token from .env

bot.run(botToken)
