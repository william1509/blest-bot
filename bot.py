# bot.py
import os

import discord
from dotenv import load_dotenv

import markovify
import random

import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

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

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    # Get raw text as string.
    with open("train.txt", 'r', encoding='utf_8') as f:
        text = f.readlines()
        random.shuffle(text)
        text = ''.join(text)

        # Build the model.
        text_model = markovify.NewlineText(text, state_size=2)
        global model
        model = text_model.compile()
        print('Model compiled')
    
    # with open("train.txt", 'w', encoding='utf_8') as f:       
    #     channels_id = [
    #         385640449244659713,
    #         442911962645659648,
    #         773034002454020116
    #     ]
    #     for id in channels_id:
    #         c_channel = client.get_channel(id)
    #         messages = await c_channel.history(limit=4000).flatten()
    #         for i in range(len(messages)):
    #             line = sanatize(messages[i].content)
    #             if 'http' in line or len(line) == 0 or 'blest' in line or messages[i].author == client.user:
    #                 continue
    #             f.write(line + '\n')
    #     print('Messages written')

@client.event
async def on_message(message):
    mess = message.content.lower()

    if message.author == client.user:
        print("Wrong user")
        return 

    if 'blest' not in mess:
        print("No blest")
        return

    response = model.make_sentence()
    while response is None:
        response = model.make_sentence()
        print("No response")
    await message.channel.send(response + " kappo")

client.run(TOKEN)
