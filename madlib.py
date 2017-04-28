import nltk, time, random, praw, re


"""
label long example
NN  singular noun ----------------------------- pyramid
NNS plural noun ------------------------------- lectures
NNP proper noun ------------------------------- Khufu
VBD past tense verb --------------------------- claimed
VBZ 3rd person singular present tense verb: --- is
VBP non-3rd person singular present tense verb: have
VBN past participle --------------------------- found
PRP pronoun ----------------------------------- they
PRP$ possessive pronoun ----------------------- their
JJ adjective ---------------------------------- public
IN preposition -------------------------------- in
complementizer -------------------------------- that
DT determiner --------------------------------- the

i think we want to use VB, NNS, NN, VBD

other thoughts are to break down the sentence
structure build better madlibs rather than
choosing words at random

"""

typeset = {'JJ': '__adjective__', 'JJS': '__adjective__', 'RB': '__adverb__', 'NNP': '__noun__', 'VB': '__verb__', 'VBN': '__verb__', 'NNS': '__plural noun__', 'NN': "__noun__", 'VBD': "__past-tense verb__" }

wordtypes = typeset.keys()

preamble = ["TIL", "TIFU"]


def madlib(title):


	tokens = nltk.pos_tag(nltk.word_tokenize(title))

	replaceable = list({word for word in tokens if word[1] in wordtypes})

	nouns = len([word[1] for word in replaceable if word[1] == 'NN'])
	total = len(replaceable)
	if total - nouns < nouns or total < 4 or "[" in title:
		# ignore too many nouns, May Have Been Submitted Like This
		# ignore boring sentences
		# ignore {Serious] threads and a lot of non-sentence topics
		return False

	numtoreplace = int(total * 0.8)

	random.shuffle(replaceable)

	to_replace = [word[0] for word in replaceable[0:numtoreplace-1]]


	#comprehend this list comprehension
	return "".join([word if word in ['.', '?', '!', ','] or "'" in word else ' ' + word for word in [typeset[word[1]].upper() if (word[0] in to_replace and word[1] in typeset) else word[0] for word in tokens]])
	#sorry mom



subreddits = ['circlejerk', 'tifu', 'todayilearned', 'news', 'nottheonion', 'askreddit', 'showerthoughts']

reddit = praw.Reddit('madlib', user_agent="badass python")

while True:

	try:
		for submission in reddit.subreddit("+".join(subreddits)).random_rising(limit=25):
			pre = ''
			title = submission.title
            
			for p in preamble:
				if title[0:len(p)] == p:
					pre = p
					title = title[len(p)+1:]

			ml = madlib(title)
			if ml:
				success = True
				try:
					submission.reply("%s%s" % (pre,ml))
				except Exception:
					success = False

				print("[%s] %s%s" % ("Success" if success else "Fail",pre,ml))
				break
	except:
		print("[Fail] !!! Unable to fetch submissions")
	time.sleep(60*random.choice(range(10,30)))

