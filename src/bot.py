# bot.py
import os
from sys import argv

import discord
from dotenv import load_dotenv
import markovify
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
        print("Wrong user")
        return 

    if 'blest' not in mess:
        print("No blest")
        return
    
    if text_model is None:
        print("Model not compiled")
        return

    response = text_model.make_short_sentence(70)
    while response is None:
        response = text_model.make_short_sentence(70)
    await message.channel.send(response + " kappo")


if __name__ == '__main__':
    client.run(TOKEN)
