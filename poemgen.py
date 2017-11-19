# POEM GENERATOR
# By Paul Broyles and Amanda Broyles
#
# Program to generate free-verse poems with sentences chosen from defined
# sentence structures.

import nltk
import random
from nltk.corpus import masc_tagged as masc

# Poem control variables
line_words_range = range(5, 8) # Range of possible line lengths
poem_lines_range = range(10, 16) # Range of possible minimum poem lengths.
# (The poem will write at least poem_lines_range lines and then end when
# the end of a sentence is reached.)

# Variable containing the possible sentence structures as a list of lists.
structs = [
    ['IN', 'ARTP', 'NNS', 'VBP', 'RB', ',', 'JJ', 'NNS', 'VBP', 'FB', 'VBP', 'RBR', '.'],
    ['ART', 'NN', ',', 'WP', 'RB', 'VBD', ',', 'VBZ', 'IN', 'ART', 'NN', 'IN', 'NNS', '.'],
    ['UH', ',', 'FW', '!', 'PSP', 'NN', 'MD', 'VB', 'TO', 'ART', 'JJ', 'NN', '.'],
    ['TO', 'VB', 'ART', 'NN', ',', 'PDT', 'ARTP', 'NNS', '--', 'JJ', 'IN', 'PSP', 'NN', '--', 'VBP', 'RB', '.'],
    ['VBG', 'VBZ', 'RB', '.'],
    ['NNS', 'VBP', 'ARTP', 'JJS', 'NNS', '.'],
    ['VB', 'EX', '.']
]

# Set up the dictionary.
cats = {}
# For each word in the tagged corpus
for word in masc.tagged_words():
    # If there's no dictionary entry for the POS
    if word[1] not in cats:
        # Add a new dictionary entry containing the current word
        cats[word[1]] = set([word[0].lower()])
    # Otherwise, unless it contains a symbol that we want to discard
    elif not('@' in word[0] or ':' in word[0] or '_' in word[0] or '.' in word[0] or '$' in word[0] or ',' in word[0] or '#' in word[0]):
            # Append it to the set for this POS
            cats[word[1]].add(word[0].lower())
# Correct dictionary errors
cats['TO'].discard('na')
cats['DT'] = set(i for i in cats['DT'] if i not in ('thei', 'de'))
cats['MD'] = set(i for i in cats['MD'] if i not in ('ca', u'\u2019ll', "'ll" 'll', 'wo', u'\u2019d', "'d"))
cats['VBZ'].discard('ai')
cats['IN'] = set(i for i in cats['IN'] if i not in ('en', 'de', 'ago', 'like', 'unlike'))
# Add new word categories.
cats['ART'] = set(['the', 'a', 'an', 'this'])
cats['ARTP'] = set(['these', 'those'])
cats['FB'] = set(['for', 'and', 'nor', 'but', 'or', 'yet', 'so'])
cats['PSP'] = set(['my', 'mine', 'your', 'his', 'her', 'their', 'its', 'our'])

# Variable containing a list of all words in the corpus; used for the title.
words = list(set(word.lower() for word in masc.words()))

# Function that accepts a sentence structure and returns a sentence of randomly
# selected words in that structure as a list.
# Structure must consist of a list of strings containing POS tags or
# punctuation marks (as recognized by the is_punctuation() function).
def build_sentence(structure):
    sent = []
    # For each item in our structure
    for item in structure:
        # If it's a punctuation mark
        if is_punctuation(item):
            # Tack it onto the end of the preceding word.
            sent[len(sent) - 1] += item
        # Otherwise
        else:
            # Choose a random word from that category and return it
            word = random_word_from_cat(item)
            # If this is the first word in the sentence,
            if len(sent) == 0:
                # append it capitalized
                sent.append(word.capitalize())
            else:
                # Otherwise, just append it in lowercase form.
                sent.append(word)
    return sent

# Function returns if an item is a punctuation mark
def is_punctuation(item):
    if item in ('.', ',', '--', '!'):
        return True
    else:
        return False

# Function returns a random word from a category
def random_word_from_cat(cat):
    return random.choice(list(word for word in cats[cat]))

# Function that returns a poem as a list of lines (each line is a string).
# Accepts the range of minimum lengths for the poem.
def build_poem(poem_lines_range):
    # Variable to contain the randomly selected length of THIS poem.
    this_poem_lines = random.choice(poem_lines_range)
    poem = []
    curr_sent = []
    # Variable to hold the line number of the current line.
    curr_line = 1
    # Variable to track whether the poem is allowed to end (i.e. has met the
    # minimum number of lines).
    done = False
    # As long as either the poem is too short or we have an unfinished sentence
    # in memory...
    while curr_line < this_poem_lines or len(curr_sent) > 0:
        # If the poem is long enough,
        if curr_line >= this_poem_lines:
            # flag that we're allowed to end.
            done = True
        # Call the function to build the line of the poem. Update the current
        # sentence based on what the function has done (i.e. consume words or
        # write a new sentence).
        curr_sent, line = build_line(curr_sent, done)
        # Turn the list of words into a string and append it to the poem.
        poem.append(' '.join(line))
        # Increment the line counter.
        curr_line += 1
    return poem

# Function to build a line of the poem. Returns the state of the current
# sentence after the line has been built and the line it has constructed.
# Accepts the current state of the current sentence and a flag telling it
# whether or not the poem may end (i.e., if it reaches the end of the
# sentence, should it begin a new one?).
def build_line(curr_sent, done):
    # Randomly set the length of THIS line.
    this_line_words = random.choice(line_words_range)
    line = []
    # For every word in a line of the defined length
    for w in range(this_line_words):
        # If there are no words in the current sentence (i.e. it's the beginning
        # of the poem or the previous sentence has ended)
        if len(curr_sent) == 0:
            # If the poem is allowed to end
            if done:
                # End the line and return it
                return curr_sent, line
            # Otherwise
            else:
                # Make a new sentence in a randomly selected structure.
                curr_sent = build_sentence(random.choice(structs))
        # Add the first word in the current sentence to the current line.
        line.append(curr_sent[0])
        # Remove the first word from the current sentence (since it's now in
        # our poem).
        curr_sent.pop(0)
    # Return the completed line (as well as the updated sentence)
    return curr_sent, line

# Function to return a single random word in all caps as the title.
def title():
    return random.choice(words).upper()

# Construct the poem.
poem = build_poem(poem_lines_range)
# Print the title followed by a blank line.
print title() + '\n'
# Print each line in the poem.
for line in poem:
    print line
