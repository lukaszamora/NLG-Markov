import random
from random import choice
import re
from collections import Counter
import nltk
from nltk.util import ngrams


def read_file(filename):
    # clean up text
    with open(filename, "r", encoding='UTF-8') as file:
        contents = file.read().replace('\n\n', ' ').replace('[edit]', '').replace(
            '\ufeff', '').replace('\n', ' ').replace('\u3000', ' ')
    return contents


text = read_file('sherlock.txt')


# First Order Markov Chain


# building a dictionary of all words with their possible next words and
# generating text based on this dictionary
# def collect_dict(corpus):
#     text_dict = {}
#     words = corpus.split(' ')
#     for i in range(len(words)-1):
#         if words[i] in text_dict:
#             text_dict[words[i]].append(words[i+1])
#         else:
#             text_dict[words[i]] = [words[i+1]]

#     return text_dict


# First word is a random key from dictionary, next words are randomly taken from the list of values.
# The text is generated until number of words reaches the defined limit.
# def generate_text(words, limit=100):
#     capitalized_keys = [i for i in words.keys() if len(i) >
#                         0 and i[0].isupper()]
#     first_word = random.choice(capitalized_keys)
#     markov_text = first_word
#     while len(markov_text.split(' ')) < limit:
#         next_word = random.choice(words[first_word])
#         first_word = next_word
#         markov_text += ' ' + next_word

#     return markov_text


# # test first order chain
# word_pairs = collect_dict(text)
# markov_text = generate_text(word_pairs, 200)
# print(markov_text, file=open('first-order.txt', 'a'))


# Second Order Markov Chain

# A better idea would be to predict next word based on two previous ones
# Now keys in dictoinary will be tuples of two words

# def collect_dict(corpus):
#     text_dict = {}
#     words = corpus.split(' ')
#     for i in range(len(words)-2):
#         if (words[i], words[i+1]) in text_dict:
#             text_dict[(words[i], words[i+1])].append(words[i+2])
#         else:
#             text_dict[(words[i], words[i+1])] = [words[i+2]]

#     return text_dict


# def generate_text(words, limit=100):
#     capitalized_keys = [i for i in words.keys() if len(
#         i[0]) > 0 and i[0][0].isupper()]
#     first_key = random.choice(capitalized_keys)

#     markov_text = ' '.join(first_key)
#     while len(markov_text.split(' ')) < limit:
#         next_word = random.choice(words[first_key])
#         first_key = tuple(first_key[1:]) + tuple([next_word])
#         markov_text += ' ' + next_word

#     return markov_text


# test second order chain
# word_pairs = collect_dict(text)
# markov_text = generate_text(word_pairs, 200)
# print(markov_text, file=open('second-order.txt', 'a'))

# tokenize instead of splitting
# def collect_dict(corpus):
#     text_dict = {}
#     words = nltk.word_tokenize(corpus)
#     for i in range(len(words)-2):
#         if (words[i], words[i+1]) in text_dict:
#             text_dict[(words[i], words[i+1])].append(words[i+2])
#         else:
#             text_dict[(words[i], words[i+1])] = [words[i+2]]

#     return text_dict


# def generate_text(words, limit=100):
#     capitalized_keys = [i for i in words.keys() if len(
#         i[0]) > 0 and i[0][0].isupper()]
#     first_key = random.choice(capitalized_keys)
#     markov_text = ' '.join(first_key)
#     while len(markov_text.split(' ')) < limit:
#         next_word = random.choice(words[first_key])

#         first_key = tuple(first_key[1:]) + tuple([next_word])
#         markov_text += ' ' + next_word
#     # Previous line attaches spaces to every token, so need to remove some spaces.
#     for i in ['.', '?', '!', ',']:
#         markov_text = markov_text.replace(' .', '.').replace(
#             ' ,', ',').replace(' !', '!').replace(' ?', '?').replace(' ;', ';')
#     return markov_text


# test
# word_pairs = collect_dict(text)
# markov_text = generate_text(word_pairs, 200)
#print(markov_text, file=open('token-text.txt', 'a'))


# Higher-order Chains
# tokenized_text = nltk.word_tokenize(text)
# n_grams = ngrams(tokenized_text, 6)
# print(Counter(n_grams).most_common(20))


# def collect_dict(corpus):
#     text_dict = {}
#     words = nltk.word_tokenize(corpus)

#     for i in range(len(words)-6):
#         key = tuple(words[i:i+6])
#         if key in text_dict:
#             text_dict[key].append(words[i+6])
#         else:
#             text_dict[key] = [words[i+6]]

#     return text_dict


# word_pairs = collect_dict(text)
# markov_text = generate_text(word_pairs, 200)
# print(markov_text, file=open('higher-order.txt', 'a'))


# Testing with Backoff
def collect_dict(corpus, n_grams):
    text_dict = {}
    words = nltk.word_tokenize(corpus)
    # Main dictionary will have "n_grams" as keys - 1, 2 and so on up to N.
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
        markov_text = markov_text.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?').replace(' ;', ';')
    return markov_text


word_pairs = collect_dict(text, 6)
markov_text = generate_text(word_pairs, 200, 6)
print(markov_text, file=open('back-off.txt', 'a'))