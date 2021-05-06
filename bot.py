import os
from datetime import datetime, timedelta
import socket
from threading import Timer

import discord
from discord.ext import commands
from dotenv import load_dotenv
from mcstatus import MinecraftServer

import asyncio
from aio_timers import Timer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='>')
# server_ip, server_port = "", ""
server_running = False

EMBED_SERVER_OFF = 0xff0000
EMBED_SERVER_ON = 0x008000
EMBED_PLAYERS = 0x00FFFF


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    timer = Timer(5, display_status)


@bot.command(name='players', help='Shows how many players are online')
async def get_players(ctx):
    status = check_status()
    print(type(status['players_online']))
    quant = 'player' if status['players_online'] == 1 else 'players'
    embed = discord.Embed(title='Players Online', description=f"{status['players_online']} {quant} online", color=EMBED_PLAYERS)
    await ctx.send(embed=embed)


@bot.command(name='status', help='Shows the current status of the server')
async def show_status(ctx):
    status = check_status()

    if status:
        embed = discord.Embed(title='Server Status', description="The server is up", color=EMBED_SERVER_ON)
    else:
        embed = discord.Embed(title='Server Status', description="The server is down", color=EMBED_SERVER_OFF)

    await ctx.send(embed=embed)


def check_status():
    server = MinecraftServer.lookup("71.244.141.99:25565")

    try:
        status = server.status()
    except Exception:
        return None

    raw = status.raw

    return {
        "text": raw['description']['text'],
        "max_players": raw['players']['max'],
        "players_online": raw['players']['online'],
        "version": raw['version']['name']
    }


async def display_status():
    status = check_status()
    channel = bot.get_channel(836290964074790912)
    global server_running

    if status is None:
        if server_running:
            server_running = False

            embed = discord.Embed(title='Server Status Update', description='Server was turned off', color=EMBED_SERVER_OFF)
            await channel.send(embed=embed)
    else:
        if not server_running:
            server_running = True

            embed = discord.Embed(title='Server Status Update', description='Server was turned on', color=EMBED_SERVER_ON)

            await channel.send(embed=embed)

    timer = Timer(5, display_status)


bot.run(TOKEN)
