# bot.py
import os, discord, asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
from Audio_files import rand_sound
from Logger import write_to_log
from Ollama_Interface import ask, question

# Load environment variables
load_dotenv("pyBot.env")
TOKEN = os.getenv('DISCORD_KEY')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL1 = os.getenv('CHANNEL_ID')
aLog = os.getenv('A_LOG')

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

        # Compare member ID to bot ID
        if member.id != 1202796878736007178:

            # Log Member Leaving
            left = f'{member} has left the voice Channel {before.channel}!\n'
            write_to_log(aLog, left)
            print(left)

            # Send Goodbye message
            await before.channel.send(f'Good bye {member}!')

            # Play exit sound
            vc = await before.channel.connect()
            source = FFmpegPCMAudio('boo-36556.mp3')
            vc.play(source)
            await timeout(vc)

    # Check if member joined
    elif before.channel is not after.channel and after.channel is not None:
        # Check if the ID is the bot
        if member.id != 1202796878736007178:

            # Log Member joining
            join = f'{member} has joined the voice Channel {after.channel}!\n'
            write_to_log(aLog, join)
            print(join)

            # Send welcome message
            await after.channel.send(f'Welcome to {after.channel}, {member}!')

            # Play random welcome sound
            vc = await after.channel.connect()
            source = FFmpegPCMAudio(rand_sound())
            vc.play(source)
            await timeout(vc)

        else:
            return

# disconnect the bot from a voice channel after a period of time
async def timeout(VoiceClient):
    await asyncio.sleep(5)
    await VoiceClient.disconnect()

# Split bot response text so it doesn't exceed the discord API 2000 char limit.
def text_splitter(input_str, chunk_size):
    return [input_str[i:i + chunk_size] for i in range(0, len(input_str), chunk_size)]

#  -------- bot commands --------
@bot.command(name="Hello!", help="Say Hello!")
async def greeting(ctx):
    response = "Hi!"
    await ctx.send(response)

@bot.command(name="?", help="Ask LLaMA2 a question from a personalized knowledgebase!")
async def ask_Kollama(ctx, *args):

    # Join multiple args as one string of text
    ask_string = ' '.join(args)
    print(ask_string)

    # Notify users a response is incoming and may take some time based off of system specs
    await ctx.send("------AI Response Incoming------")

    # Send user question to AI
    response = str(ask(ask_string))

    # Discord API errors on responses larger than 2000 char.
    # Break up chars into chunks less than 2000 char and send to server
    if len(response) > 2000:
        chunk_arr = text_splitter(response, 1900)
        print("chunking...")
        for chunks in chunk_arr:
            await ctx.send(chunks)
    else:
        await ctx.send(response)

@bot.command(name="!", help="Ask LLaMA2 a question!")
async def ask_ollama(ctx, *args):

    # Join multiple args as one string of text
    ask_string = ' '.join(args)
    print(ask_string)

    # Notify users a response is incoming and may take some time based off of system specs
    await ctx.send("------AI Response Incoming------")

    # Send user question to AI
    response = str(question(ask_string))

    # Discord API errors on responses larger than 2000 char.
    # Break up chars into chunks less than 2000 char and send to server
    if len(response) > 2000:
        chunk_arr = text_splitter(response, 1900)
        print("chunking...")
        for chunks in chunk_arr:
            await ctx.send(chunks)
    else:
        await ctx.send(response)
bot.run(TOKEN)
