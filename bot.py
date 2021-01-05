import sys
import discord

try:
	token = sys.argv[1]
except IndexError:
	print("Didn't get a token! Run \"py bot.py <token here>\" to launch the bot.")
	sys.exit(1) #exit with error, we don't need to do anything else w/o a token
	
parsed_stories = []
	
class Story:
	text = ""
	to_replace = {}
	
	def parse_text(self, text):
		self.text = text
		#get each word that starts with $ and put it in to_replace
		for x in text.split():
			if x.startswith("$"):
				self.to_replace[x] = ""

	def __init__(self, text):
		#self.text = text
		self.parse_text(text)
		

client = discord.Client() #making a new client object

@client.event
async def on_ready():
	print("Bot connected as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.content.startswith("!test"):
		await message.channel.send("Hello world")

def read_stories():
	print("Reading stories...")
	f = open("stories.txt", "rt", encoding="UTF-8")
	#iterate through each story, separated by a newline, and new up a Story object for each
	#TODO: if no stories (try-catch?), print an error message, possibly exit
	stories_raw = f.read()
	f.close()
	stories_raw = stories_raw.splitlines()
	print("Parsing stories...")
	for s in stories_raw:
		#pulling out the words to replace is done in Story.parse_text()
		#just make the new story and give it its text here
		new_story = Story(s)
		#and put it in parsed_stories
		parsed_stories.append(new_story)
	print("Done. I have " + str(len(parsed_stories)) + " stories.")



#read stories in here
read_stories()
client.run(token)

