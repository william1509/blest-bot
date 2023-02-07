# blest-bot

## Installing dependencies

Run the following to install the required pip packages

`pip install -r requirements.txt`

## Setup environnement file

You need to create a file named `.env` and place the following inside

```
# .env
DISCORD_TOKEN={YOUR_DISCORD_TOKEN_HERE}
DISCORD_GUILDS={TEXT_CHANNEL_IDS}
TRIGGER_WORD={TRIGGER_WORD}
SUFFIX_WORD={SUFFIX_WORD}
```

Example:

```
# .env
DISCORD_TOKEN=488494944994
DISCORD_GUILDS=437289473289,43829042389,4738294279
TRIGGER_WORD=blest
SUFFIX_WORD=kappo
```
Watch out ! The text channel ids must be separated by a comma `,`

## Create the training file

The script `training_set_generator.py` creates the `train_1.txt` file containing the 4000 last messages from the channels in the `.env` file

To start the script simply execute the following line

`python3 training_set_generator.py`

If you want to make your own training file, simply create a file named `train_X.txt` where X is any integer. Make sure each sentences are separeted by a new line, like the following :

```
This is a sentence
This is another sentence
```

## Start the bot

You can either start the bot in your terminal with

`python3 bot.py`

or as a background process with 

`python3 bot.py > logs.txt &`

Using docker, you can simply run `docker compose run blest-bot-training` to run the training program and `docker compose run blest-bot-svc` to run the actual bot

## Stop the bot

To stop the bot, you can simply kill the process with `Ctrl + C` if it runs inside a terminal or you can find its PID with `pgrep -lf python3` if it's running in the background.
