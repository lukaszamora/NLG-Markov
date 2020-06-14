# NLG-Markov
Natural Language Generation with Markov Chains


Natural language generation (NLG) means creating new text based on some given raw text. Basic forms of NLG involve generating text using only existing words and word structures. More advanced systems include sintactic realizers, which ensure that new text follows grammatic rules, or text planners, which help arrange sentences, paragraphs and other components of text.

Automatical text generation can be used for a variety of tasks, among others:

* Automatic documentation generation;
* Automatic reports from raw data;
* Explanations in expert systems;
* Machine translation between natural languages;
* Chatbots

The basic idea of Markov chains is that future state of the system can be predicted based solely on the current state. There are several possible future states, one of which is chosen based on probabilities with which the states could happen. Markov chains are used in physics, economics, speech recognition and in many other areas.

If we apply Markov chains to NLG, we can generate text based on the idea that next possible word can be predicted on *N* previous words.

In this project I'll start with generating text based only on one previous word, and then will try to improve the quality of predictions.

```
import random
from random import choice
import re
from collections import Counter
import nltk
from nltk.util import ngrams
```

## Data Preparation
I use "The Adventures of Sherlock Holmes" by Arthur Conan Doyle to generate text in this project. The book is downloaded from Project Gutenberg [site](https://www.gutenberg.org/files/1661/1661-0.txt).

```
def read_file(filename):
    with open(filename, "r", encoding='UTF-8') as file:
    	contents = file.read().replace('\n\n',' ').replace('[edit]', '').replace('\ufeff', '').replace('\n', ' ').replace('\u3000', ' ')
    return contents
    
text = read_file('sherlock.txt')
```

## First-order Markov Chain
The code consists of two parts: building a dictionary of all words with their possible next words and generating text based on this dictionary.

Text is splitted into words. Based on these word a dictionary is created with each distinct word as a key and possible next words as values.

After this the new text is generated. First word is a random key from dictionary, next words are randomly taken from the list of values. The text is generated until number of words reaches the defined limit.

```
def collect_dict(corpus):
	text_dict = {}
	words = corpus.split(' ')
	for i in range(len(words)-1):
		if words[i] in text_dict:
			text_dict[words[i]].append(words[i+1])
		else:
			text_dict[words[i]] = [words[i+1]]
	return text_dict

def generate_text(words, limit = 100):
	first_word = random.choice(list(words.keys()))
	markov_text = first_word
	while len(markov_text.split(' ')) < limit:
		next_word = random.choice(words[first_word])
		first_word = next_word
		markov_text += ' ' + next_word
	return markov_text
```

```
word_pairs = collect_dict(text)
markov_text = generate_text(word_pairs, 200)
print(markov_text, file=open('first-order.txt', 'a'))
```

```
Nearly all that they could show you doing there. In the sufferer. It is quite follow your uncle, to advance from Waterloo. It may want your watch-chain, the sort of poetry. Then there may not but the corner of his hands, spoke her letters when examining it, but swayed his stick two of the bridegroom), and sticks.
```

And here we have it - the generated text. Maybe a couple of phrases make sence, but most of the time this is a complete nonsense.

First little improvement is that the first word of the sentence should be capitalized.

So now the first word will be chosen from the list of capitalized keys.

```
def generate_text(words, limit = 100):
	capitalized_keys = [i for i in words.keys() if len(i) > 0 and i[0].isupper()]
	first_word = random.choice(capitalized_keys)
	markov_text = first_word
	while len(markov_text.split(' ')) < limit:
		next_word = random.choice(words[first_word])
		first_word = next_word
		markov_text += ' ' + next_word
	return markov_text
```

```
The smell of its conventionalities and the point. He found, as a note was seven weeks elapsed between the room, and threw all theories to fill me that two hours passed his armchair and two days to the three or online at all.
```

A bit better. It's time to go deeper.

## Second-order Markov Chain
First-order Markov chains give a very randomized text. A better idea would be to predict next word based on two previous ones. Now keys in dictoinary will be tuples of two words.

```
def collect_dict(corpus):
	text_dict = {}
	words = corpus.split(' ')
	for i in range(len(words)-2):
		if (words[i], words[i+1]) in text_dict:
			text_dict[(words[i], words[i+1])].append(words[i+2])
		else:
			text_dict[(words[i], words[i+1])] = [words[i+2]]

	return text_dict


def generate_text(words, limit=100):
	capitalized_keys = [i for i in words.keys() if len(
		i[0]) > 0 and i[0][0].isupper()]
	first_key = random.choice(capitalized_keys)

	markov_text = ' '.join(first_key)
	while len(markov_text.split(' ')) < limit:
		next_word = random.choice(words[first_key])
		first_key = tuple(first_key[1:]) + tuple([next_word])
		markov_text += ' ' + next_word

	return markov_text
```

```
word_pairs = collect_dict(text)
markov_text = generate_text(word_pairs, 200)
print(markov_text)
```

```
Holmes walked slowly up the epistle. He says four o'clock. It is absolutely all that district, and there was a singular chance has placed in so frightful a form, have been recommended to me, Ryder, that there are points in it I heard my father I looked again there he was able to look sleepily from their traces. "Yes, they have been cruelly used", said Holmes.
```

Now more sentences make sense.

## Tokenizing instead of splitting
But there are a lot of problems with punctuation. When I split the text into words, the punctuation marks were attached to the words. To solve this problem I can consider them being separate words. Let's try.

```
def collect_dict(corpus):
	text_dict = {}
	words = nltk.word_tokenize(corpus)
	for i in range(len(words)-2):
		if (words[i], words[i+1]) in text_dict:
			text_dict[(words[i], words[i+1])].append(words[i+2])
		else:
			text_dict[(words[i], words[i+1])] = [words[i+2]]

	return text_dict
  
def generate_text(words, limit = 100):
	capitalized_keys = [i for i in words.keys() if len(i[0]) > 0 and i[0][0].isupper()]
	first_key = random.choice(capitalized_keys)
	markov_text = ' '.join(first_key)
	while len(markov_text.split(' ')) < limit:
		next_word = random.choice(words[first_key])

	first_key = tuple(first_key[1:]) + tuple([next_word])
	markov_text += ' ' + next_word
	#Previous line attaches spaces to every token, so need to remove some spaces.
	for i in ['.', '?', '!', ',']:
		markov_text = markov_text.replace(' .', '.').replace(' ,', ',').replace(' !',
		'!').replace(' ?', '?').replace(' ;', ';')
	return markov_text
```

```
word_pairs = collect_dict(text)
markov_text = generate_text(word_pairs, 200)
print(markov_text, file=open('token-text.txt', 'a'))
```

```
But I can not blame you, but Holmes caught me by the approach of Peterson, so I shall soon know which to base my articles and thought little of its force. Perhaps I had my rubber. I think that perhaps he was only a few days I would always carry the case complete. You must be where she sat for a bed fastened like that.
```

## Higher-order Markov Chain
For a little text predicting next word based on two previous is justified, but large texts can use more words for prediction without fearing overfitting. Let's see the list of 6-grams.

```
tokenized_text = nltk.word_tokenize(text)
n_grams = ngrams(tokenized_text, 6)
Counter(n_grams).most_common(20)
```

```
[(('to', 'the', 'Project', 'Gutenberg', 'Literary', 'Archive'), 24),
	((',', 'Watson', ',', '—', 'said', 'he'), 21),
	((',', 'Watson', ',', '—', 'said', 'Holmes'), 15),
	(('.', 'On', 'the', 'other', 'hand', ','), 13),
	((',', '—', 'said', 'he', ',', '—that'), 5),
	((',', '—', 'said', 'Holmes', ',', 'laughing'),5),
	(('I', 'think', ',', 'Watson', ',', 'that'),5),
	((',', '—', 'said', 'he', '.', '—I'), 5),
	(('?', '—', '—Yes', ',', 'sir', '.'), 5),
	(('from', 'one', 'to', 'the', 'other', 'of'),5),
	((',', '—', 'said', 'he', ',', '—but'), 5),
	(('one', 'to', 'the', 'other', 'of', 'us'), 5),
	((',', '—', 'said', 'he', '.', '—It'), 5),
	(('the', 'air', 'of', 'a', 'man', 'who'), 4),
	(('.', 'Still', ',', 'of', 'course', ','), 4),
	(('with', 'the', 'air', 'of', 'a', 'man'), 4),
	(('the', 'phrase', '``', 'Project', 'Gutenberg', "''"), 4),
	((',', 'Mr.', 'Holmes', ',', 'and', 'I'), 4),
	(('Watson', ',', '—', 'said', 'he', ','), 4)]
```

What a talkative count! Well, the point is that it is quite possible to use 6 words, let's try.

```
def collect_dict(corpus):
	text_dict = {}
	words = nltk.word_tokenize(corpus)
	for i in range(len(words)-6):
		key = tuple(words[i:i+6])
		if key in text_dict:
			text_dict[key].append(words[i+6])
		else:
			text_dict[key] = [words[i+6]]

	return text_dict
```

```
word_pairs = collect_dict(text)
markov_text = generate_text(word_pairs, 200)
print(markov_text)
```

```
We would not dare to conceive the things which are really mere commonplaces of existence. If we could fly out of that window hand in hand, hover over this great city, gently remove the roofs, and peep in at the queer things which are going on, the strange coincidences, the plannings, the cross-purposes, the wonderful chains of events, working through generations, and leading
```

Sadly, we have a severe overfitting!

## Backoff
One of the ways to tackle it is back-off. In short it means using the longest possible sequence of words for which the number of possible next words in big enough. The algorithm has the following steps:

* for a key with length *N*  check the number of possible values;
* if the number is higher that a defined threshold, select a random word and start algorithm again with the new key;
* if the number is lower that the threshold, then try a taking *N-1* last words from the key and check the number of possible values for this sequence;
* if the length of the sequence dropped to one, then the next word is randomly selected based on the original key;

Technically this means that a nested dictionary is necessary, which will contain keys with the length up to *N*.

```
def collect_dict(corpus, n_grams):
	text_dict = {}
	words = nltk.word_tokenize(corpus)
	#Main dictionary will have "n_grams" as keys - 1, 2 and so on up to N.
	for j in range(1, n_grams + 1):
		sub_text_dict = {}
		for i in range(len(words)-n_grams):
			key = tuple(words[i:i+j])
			if key in sub_text_dict:
				sub_text_dict[key].append(words[i+n_grams])
			else:
				sub_text_dict[key] = [words[i+n_grams]]
		text_dict[j] = sub_text_dict

	return text_dict

def get_next_word(key_id, min_length):
	for i in range(len(key_id)):
		if key_id in word_pairs[len(key_id)]:
			if len(word_pairs[len(key_id)][key_id]) >= min_length:
				return random.choice(word_pairs[len(key_id)][key_id])
		else:
			pass
		if len(key_id) > 1:
			key_id = key_id[1:]
	return random.choice(word_pairs[len(key_id)][key_id])

def generate_text(words, limit = 100, min_length = 5):
	capitalized_keys = [i for i in words[max(words.keys())].keys() if len(i[0]) > 0 and i[0][0].isupper()]
	first_key = random.choice(capitalized_keys)
	markov_text = ' '.join(first_key)
	while len(markov_text.split(' ')) < limit:
		next_word = get_next_word(first_key, min_length)
		first_key = tuple(first_key[1:]) + tuple([next_word])
		markov_text += ' ' + next_word
	for i in ['.', '?', '!', ',']:
		markov_text = markov_text.replace(' .', '.').replace(' ,', ',').replace('
		!', '!').replace(' ?', '?').replace(' ;', ';')
	return markov_text
```

```
word_pairs = collect_dict(text, 6)
markov_text = generate_text(word_pairs, 200, 6)
print(markov_text)
```

```
Well think manner seldom, as of leaves the knew sealed. Captain Star-will a million other out. Stood, terms the presently astonishment some many hearing father.
```

That's it. This is as far ar simple Markov chains can go. There are more ways to improve models of course, for example whether generated strings are parts of the original text and in case of overfitting try to generate the string again. Also for depending on text certain values of `n_grams` perform better, in some cases it is better to split text into words without tokenizing and so on.

Here are some interesting phrases/sentences which were generated:
* My life is spent in one long effort to escape from the commonplaces of existence.
* Have pity on me, but I suppose it would be the punishment that possibly I may fairly and freely accept your invitation, having promised to remain as one of the narrator. Watson knows everybody.
* there’s liberty for revenge by not eating or drinking
* Then he drew a paper in the manner of saying “No.” “No?” said Watson
* I would not desire any other affliction which would have been on the sandy beach
* We would not dare to conceive the things which are really mere commonplaces of existence.
* And you are a benefactor of the race, said I.
