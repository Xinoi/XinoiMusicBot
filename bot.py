import discord
from discord.ext import commands
from pytube import YouTube, Search
import os
import audiofile

TOKEN = 'MTA3NTQwMDU5MzI0NzU2NzkwMg.GJ2jCv.tsgEN8n5rxln6IWTaIN5wj4mnX2x1A8ZNkYURc'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

#get youtube mp3
async def getAudio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(os.getcwd())
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return base + ".mp3"

@bot.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("-Im not in a voice channel-")
        return

@bot.command(name='play')
async def play(ctx, url):
    author = ctx.message.author
    channel = author.voice.channel
    voice_channel = ctx.message.guild.voice_client
    #if voice_channel.is_playing():
        #await ctx.send("-trying to connect-")
    #else:
        #await ctx.send("-already playing-")
    if author.voice:
        await channel.connect()
    else:
        await ctx.send("please connect to voice channel!")
    try:
        filename = await getAudio(url)
        await ctx.send("-playing-" + filename)
        voice_channel.play(discord.FFmpegPCMAudio(source=filename))
    except:
        await ctx.send("-UUPS that didnt work -> try it like this: !play [Youtube Link]-")
        await voice_channel.disconnect()
bot.run(TOKEN)