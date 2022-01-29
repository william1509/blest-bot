# bot.py
import os

import discord
from dotenv import load_dotenv
import markovify
import random

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("Token not found")
    exit(1)

TRIGGER_WORD = str(os.getenv('TRIGGER_WORD'))
if TRIGGER_WORD is None:
    TRIGGER_WORD = 'blest'

SUFFIX_WORD = str(os.getenv('SUFFIX_WORD'))
if SUFFIX_WORD is None:
    SUFFIX_WORD = ''


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    models = []
    models_weights = []

    directory = os.listdir(".")

    directory = [ a for a in directory if 'train' in a and a.endswith('.txt')]

    if len(directory) == 0:
        await client.close()
        return

    for file in directory:
        if 'train' in file and file.endswith(".txt"):
    
            with open(file, 'r', encoding='utf_8') as f:
                text = f.readlines()
                random.shuffle(text)
                text = ''.join(text)

                # Build the model.
                models.append(markovify.NewlineText(text, state_size=2))
                models_weights.append(1)
    
    model_combo = markovify.combine(models, models_weights)

    global text_model
    text_model = model_combo.compile()
                
    print('Model compiled')

@client.event
async def on_message(message):
    mess = message.content.lower()

    if message.author == client.user:
        print("Bot message")
        return 

    if TRIGGER_WORD not in mess:
        print("No trigger word")
        return
    
    if text_model is None:
        print("Model not compiled")
        return

    response = text_model.make_short_sentence(70)
    while response is None:
        response = text_model.make_short_sentence(70)
    await message.channel.send(response + SUFFIX_WORD)


if __name__ == '__main__':
    client.run(TOKEN)
