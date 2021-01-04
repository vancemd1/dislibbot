import sys
import discord
try:
	token = sys.argv[1]
except IndexError:
	print("Didn't get a token! Run \"py bot.py <token here>\" to launch the bot.")
	sys.exit(1) #exit with error, we don't need to do anything else w/o a token

client = discord.Client() #making a new client object

@client.event
async def on_ready():
	print("Bot connected as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.content.startswith("!test"):
		await message.channel.send("Hello world")
		print("Sent response, exiting.")


client.run(token)

