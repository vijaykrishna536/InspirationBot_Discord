import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


my_secret = os.environ['token']
client = discord.Client()

sad_words = ["sad", "angry", "depressed", "unhappy", "misrable", "lonely"]

encougarement_words = ["Cheer Up!", 
"Hang In There!!", 
"You are doing just fine"]

if "respond" not in db.keys():
  db["respond"] = True


def update_encouragements(encouragement_message):
  if "encouragements" in db.keys():
    encouragements = list(db["encouragements"])
    encouragements.append(encouragement_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouragement_message]

def delete_encouragements(index):
  encouragements = list(db["encouragements"])
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_quote():
  response = requests.get("https://zenquotes.io/api/random/")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as the {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user: 
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)


  if db["respond"]:
    options = encougarement_words
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith('$contribute'):
    encouragement_message = message.content.split("$contribute ",1)[1]
    update_encouragements(encouragement_message)
    await message.channel.send("New encouragement added!!")

  if message.content.startswith('$del'):
    encouragements_list = []

    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragements(index)
      encouragements_list = list(db["encouragements"])

    await message.channel.send(encouragements_list)

  if message.content.startswith('$get'):
    encouragements_list = []

    if "encouragements" in db.keys():
      encouragements_list = list(db["encouragements"])

    await message.channel.send(encouragements_list)

  if message.content.startswith('$encourage'):
    encourage = message.content.split("$encourage ",1)[1]
    if encourage.lower() == "true":
      db["respond"] = True
      await message.channel.send("Encourage Enabled")
    else:
      db["respond"] = False
      await message.channel.send("Encourage Disabled")
    

keep_alive()
client.run(my_secret)