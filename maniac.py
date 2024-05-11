from discord.ext import commands
from dotenv import load_dotenv
import discord 
from discord import Message
import asyncio
import yt_dlp
import os
import typing as t
import datetime as dt
import enum
import random
import re
from responses import get_response

class QueueIsEmpty(commands.CommandError):
    pass


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    client = commands.Bot(command_prefix="?", intents=intents)

    voice_clients = {}
    queues = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

    @client.event
    async def on_ready():
        print(f'{client.user} is now jamming')

    async def play_next(ctx):
        if queues[ctx.guild.id] != []:
            # Fetch the first song in the queue
            link = queues[ctx.guild.id].pop(0)
            await play(ctx, link)

    @client.command(name="play")
    async def play(ctx, link):
        try:
            if ctx.author.voice is None:
                return await ctx.send("Vào voice đi đã ccho")
            
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        except Exception as e:
            print(e)
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
        except Exception as e:
            print(e)

    @client.command(name="clear_queue")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("Có mẹ j đâu mà clear")

    @client.command(name="pause")
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    @client.command(name="resume")
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    @client.command(name="stop")
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @client.command(name="add")
    async def queue(ctx, url):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(url)
        await ctx.send("Đã thêm vào playlist!")

    @client.command(name="skip")
    async def skip(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await play_next(ctx)
            await ctx.send('Skip qua bài hát kế tiếp!')
        except Exception as e:
            print(e)

    @client.command(name='acdi')
    async def acdi(ctx):
        try:
            await ctx.send('ngoai thanh')
        except Exception as e:
            print(e)

    


    

    
        


    client.run('MTIyMjQ4OTgwMzAyMzU4MTIwNA.G0tkYE.nwhpsb55CVH-CFjiFbXjtr_QSFsP8Nqt7Jmiwc')

