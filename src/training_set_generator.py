from facebook_scraper import get_posts
import discord
from dotenv import load_dotenv
import os
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNELS = os.getenv('DISCORD_GUILDS')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def sanatize(test_str):
    ret = ''
    skip1c = 0
    for i in test_str:
        if i == '<':
            skip1c += 1
        elif i == '>' and skip1c > 0:
            skip1c -= 1
        elif skip1c == 0:
            ret += i
    return ret.lower()

async def train_discord():
    with open("training/train.txt", 'w', encoding='utf_8') as f:
        """ Get discord messages"""
        for id in CHANNELS.split(','):
            c_channel = client.get_channel(int(id))
            history = c_channel.history(limit=4000)
            messages = [i async for i in history]
            for i in range(len(messages)):
                line = sanatize(messages[i].content)
                if len(line) == 0 or \
                'http' in line or \
                'blest' in line or \
                '@everyone' in line or \
                ';;' in line or \
                messages[i].author == client.user:
                    continue
                f.write(line + '\n')

        print('Messages written')
        f.close()
    print('Discord messages written')

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    await train_discord()
    await client.close()
    

if __name__ == '__main__':
    # Clear the training files
    directory = os.listdir(".")

    for file in directory:
        if 'train' in file and file.endswith(".txt"):
            os.remove(file)

    # Add the messages from facebook
    if TOKEN is None or TOKEN == "":
        print("The token is empty")
        exit(0)

    # Add the messages from discord
    client.run(TOKEN)
