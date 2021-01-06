import sys
import random
import discord

try:
	token = sys.argv[1]
except IndexError:
	print("Didn't get a token! Run \"py bot.py <token here>\" to launch the bot.")
	sys.exit(1) #exit with error, we don't need to do anything else w/o a token

parsed_stories = []
current_story = None

class Story:
	def parse_text(self, text):
		#get each word that starts with $ and put it in to_replace
		for x in text.split():
			if x.startswith("$"):
				#multiple instances of the same word will only make one key in to_replace
				self.to_replace[x] = None

	def __init__(self, text):
		self.text = text
		self.to_replace = {}
		self.parse_text(text)

def read_stories():
	print("Reading stories...")
	f = open("stories.txt", "rt", encoding="UTF-8")
	#iterate through each story, separated by a newline, and make a Story object for each
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

def start_story():
	#Python oddity: Global variables must be explicitly declared as such within a code
	#block if they are ASSIGNED a value there, otherwise the interpreter defaults to
	#assuming you want to use a local variable. This is problematic in this case since
	#if we didn't have the global statement, then we're trying to reference the
	#supposedly local current_story before declaring it in this scope.
	global current_story
	if current_story == None:
		current_story = random.choice(parsed_stories)
		return True
	else:
		return False

#Scalability consideration: Repeatedly iterating over the current story's words to
#replace is a bit expensive, but it's easier to find it each time than to try to
#track the next word globally. If this bot somehow got popular and on a lot of servers
#then this is something that ought to be refactored.

def get_next_word():
	#get current_story's next blank word in its to_replace
	for key in iter(current_story.to_replace):
		if current_story.to_replace[key] == None:
			return key
	#if we get here then there are no more blanks
	return None

def add_next_word(submitted_word):
	global current_story
	#take submitted_word and store it into current_story's next blank to_replace value
	next = get_next_word()
	#TODO: maybe do a check here to see if it returned None, just in case
	current_story.to_replace[next] = submitted_word

def reset_story():
	#clear current_story and such
	global current_story
	for key in current_story.to_replace:
		current_story.to_replace[key] = None
	current_story = None
	return

def story_done():
	completed_story = current_story.text
	for key in iter(current_story.to_replace):
		completed_story = completed_story.replace(key, current_story.to_replace[key])
	reset_story()
	return completed_story

def make_prompt_for_word(word):
	#passed in word is going to be something like $PRESENT_TENSE_VERB
	#mung it into "present tense verb" and return a nice message asking for that
	return_str = "This is the next word I need: **"
	return_str += word.lstrip("$").lower().replace("_", " ")
	return_str += "**\nSubmit words or phrases using `!word [your words go here]`."
	return return_str

client = discord.Client()

@client.event
async def on_ready():
	print("Bot connected as {0.user}".format(client))

@client.event
async def on_message(message):
	#TODO: refactor with a switch statement, or something more elegant than a chain of ifs
	if message.content.startswith("!test"):
		await message.channel.send("Hello world")
	elif message.content.startswith("!story"):
		if start_story():
			start_str = "Okay! I have a story and I need your help filling in the blanks.\n"
			print("Starting a story: \"" + str(current_story.text[0:30]) + "...\"")
			start_str += make_prompt_for_word(get_next_word())
			await message.channel.send(start_str)
		else:
			await message.channel.send("We're already doing a story.")
	elif message.content.startswith("!word"):
		if current_story != None:
			submitted_word = message.content.split(" ", 1)[1]
			add_next_word(submitted_word)
			next = get_next_word()
			next_str = "Got it! \"**" + submitted_word + "**\"\n"
			if next == None:
				next_str += "And the story's all done, too!\n\n"
				next_str += story_done() + "\n\n"
				next_str += "I'm ready for a new story. Use `!story` to start again."
			else:
				next_str += make_prompt_for_word(next)
			await message.channel.send(next_str)
		#else discard
	elif message.content.startswith("!reset"):
		#TODO: consider limiting !reset to server admins, or similar
		reset_story()
		await message.channel.send("Okay, I have reset the story.")


#read stories in here
read_stories()
client.run(token)

