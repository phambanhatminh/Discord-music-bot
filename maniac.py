
from dotenv import load_dotenv
import discord
from discord.ext import commands
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
    print(f" Token is: {TOKEN}")
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
        if ctx.guild.id in queues and queues[ctx.guild.id]:
            song_info = queues[ctx.guild.id].pop(0)
            query = song_info['url']

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        if 'entries' in data:
            data = data['entries'][0]

        title = data.get('title', 'Unknown Title')
        url = data['url']
        player = discord.FFmpegOpusAudio(url, **ffmpeg_options)

        voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
        await ctx.send(f"🎶 Now playing: **{title}**")

    @client.command(name="play")
    async def play(ctx, *, query):
        try:
            if ctx.author.voice is None:
                return await ctx.send("Join a voice channel first!")
            
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        except Exception as e:
            print(e)
        try:
            loop = asyncio.get_event_loop()


            if not re.match(r'^https?://', query):
                query = f'ytsearch:{query}'
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))

            if 'entries' in data:
                data = data['entries'][0]
            
            song = data['url']
            title = data.get('title', 'Unknown Title')
            webpage_url = data.get('webpage_url', 'Unknown URL')

            if voice_clients[ctx.guild.id].is_playing() or queues.get(ctx.guild.id):
                if ctx.guild.id not in queues:
                    queues[ctx.guild.id] = []
                queues[ctx.guild.id].append({
                    'title': title,
                    'url': webpage_url
                })
                return await ctx.send(f"Added **{title}** to the queue!")
            
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)


            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
            await ctx.send(f"Now playing: **{title}**")
        except Exception as e:
            print(e)

    @client.command(name="clear_queue")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("There is nothing to clear.")

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

    @client.command(name="queue")
    async def show_queue(ctx):
        if ctx.guild.id not in queues or not queues[ctx.guild.id]:
            return await ctx.send("📭 Queue is empty!")

        message = "🎶 **Current Queue:**\n"
        for i, song in enumerate(queues[ctx.guild.id], start=1):
            message += f"{i}. {song['title']}\n"

        await ctx.send(message)
    @client.command(name="stop")
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)
        await ctx.send("Stopped and disconnected from the voice channel.")

    @client.command(name="skip")
    async def skip(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await ctx.send('Skip to the next song!')
        except Exception as e:
            print(e)

    @client.command(name='acdi')
    async def acdi(ctx):
        try:
            await ctx.send('ngoai thanh')
        except Exception as e:
            print(e)

    client.run(TOKEN)

