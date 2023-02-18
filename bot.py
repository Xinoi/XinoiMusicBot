import discord
from discord.ext import commands
from pytube import YouTube, Search
import os
import audiofile

TOKEN = 'MTA3NTQwMDU5MzI0NzU2NzkwMg.GyBrkj.Altl7gLVuR-SkaumnPyTn7ridE0R1Uxg6GpIwo'

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
    return yt.title + ".mp3"

@bot.command(name='join')
async def join(ctx):
    author = ctx.message.author
    await ctx.send("-trying to connect-")
    if author.voice:
        channel = author.voice.channel
        await channel.connect()
    else:
        await ctx.send("please connect to voice channel!")

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
    server = ctx.message.guild
    voice_channel = server.voice_client
    filename = await getAudio(url)
    await ctx.send("playing: " + filename)
    voice_channel.play(audiofile.read(discord.FFmpegPCMAudio(source=filename)))
        
bot.run(TOKEN)