import os
from datetime import datetime, timedelta
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


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    timer = Timer(5, display_status)


# @bot.command(name='set', help='Sets the server ip and port')
# async def set_ip_and_port(ctx, ip, port='25565'):
#     server_ip = ip
#     server_port = port
#     test = server_ip + ':' + server_port
#     await ctx.send(f"Updated server infomation\nBot will check if server is running on {test}")


def check_status():
    server = MinecraftServer.lookup("71.244.141.99:25565")

    try:
        status = server.status()
    except socket.timeout:
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
