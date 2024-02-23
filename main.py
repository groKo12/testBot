# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import Audio_files

# Load environment variables
load_dotenv("pyBot.env")
TOKEN = os.getenv('DISCORD_KEY')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL1 = os.getenv('CHANNEL_ID')

# set intents variable that is called in 'bot'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

# instantiate bot & client
bot = commands.Bot(intents=intents, command_prefix='!')
channel = bot.get_channel(CHANNEL1)


# lmk when connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    print(f'{member} has connected to {channel}!')
    await channel.send(f'Welcome to {GUILD}, {member}!')


@bot.event
async def on_voice_state_update(member, before, after):
    # Check if member left
    if before.channel is not None and after.channel is not before.channel:
        if member.id != 1202796878736007178:
            print(f'{member} has left the voice Channel {before.channel}!')
            await before.channel.send(f'Good bye {member}!')
            vc = await before.channel.connect()
            source = FFmpegPCMAudio('boo-36556.mp3')
            vc.play(source)
            await timeout(vc)

    # Check if member joined
    elif before.channel is not after.channel and after.channel is not None:
        if member.id != 1202796878736007178:
            print(f'{member} has joined the voice Channel {after.channel}!')
            await after.channel.send(f'Welcome to {after.channel}, {member}!')
            vc = await after.channel.connect()
            source = FFmpegPCMAudio(Audio_files.rand_sound())
            vc.play(source)
            await timeout(vc)
        else:
            return

async def timeout(VoiceClient):
    await asyncio.sleep(5)
    await VoiceClient.disconnect()

# bot commands
@bot.command(name="Hello!", help="Say Hello!")
async def greeting(ctx):
    response = "Hi!"
    await ctx.send(response)


bot.run(TOKEN)
