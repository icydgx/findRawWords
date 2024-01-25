# -*- coding: utf-8 -*-

# Importing necessary libraries
import re
import os
from types import NoneType
import stardict
import re
import time

# Creating an instance of the LemmaDB class from the stardict module
lemma = stardict.LemmaDB()

# Loading the lemma database from 'lemma.en.txt' file
t = time.time()
lemma.load('lemma.en.txt')
print('load in %s seconds' % str(time.time() - t))

# Function to find unknown words in a given text file
def find_unknown_words(text_file, word_list_file):
    # Reading the contents of the text file
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Removing curly braces and their contents from the text
    text = re.sub(r"\{.*?\}", "", text)

    # Filtering out non-alphabetic characters and converting them to spaces
    filtered_text = re.sub(r"[^a-zA-Z\s]+", ' ', text)

    # Extracting words from the filtered text
    words = re.findall(r"\b[a-zA-Z']+\b", filtered_text)

    # Filtering out words containing apostrophes
    words = [word for word in words if "'" not in word]

    # Filtering out words starting with uppercase letters
    words = [word for word in words if not word[0].isupper()]

    # Reading the word list file
    with open(word_list_file, 'r', encoding='utf-8') as file:
        word_list = file.read().lower().splitlines()

    # Set to store unknown words
    unknown_words = set()

    # Checking each word for its stem in the lemma database
    for word in words:
        result = lemma.word_stem(word.lower())
        if result is not None:
            # Checking conditions for unknown words
            if text_file.lower().endswith('.srt') or text_file.lower().endswith('.txt'):
                if len(word) > 3 and str(result[0]) not in word_list:
                    if len(str(result[0])) == 3 and str(result[0]).endswith('s'):
                        continue
                    unknown_words.add(word)

    # Converting the set of unknown words to a sorted list
    unknown_words = list(unknown_words)
    unknown_words.sort()

    # Returning the list of unknown words
    return unknown_words

# Folder containing text files
text_folder = 'raw_word'

# Selecting the first text file in the folder
text_file = os.listdir(text_folder)[0]

# Word list file
word_list_file = "knew_word_list.txt"

# Finding unknown words in the selected text file
unknown_words = find_unknown_words(os.path.join(text_folder, text_file), word_list_file)

# Printing each unknown word
for i in unknown_words:
    print(i)

# Printing the total number of unknown words
print(len(unknown_words))
