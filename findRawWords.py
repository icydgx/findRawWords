# -*- coding: utf-8 -*-

import re
import os
from types import NoneType
import sys

# Add the path of the dictionary module
sys.path.append('C:/python/ECDICT-master')
import stardict
import re
import time

# Function to remove duplicate words from a text
def remove_duplicates(text):
    words = text.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return ' '.join(unique_words)

# Add current directory to the sys.path
sys.path.append('.')

# Create a LemmaDB object
lemma = stardict.LemmaDB()

# Load the lemma dictionary
t = time.time()
lemma.load('C:/python/ECDICT-master/lemma.en.txt')
print('load in %s seconds' % str(time.time() - t))

# Function to find unknown words in a text file
def find_unknown_words(text_file, word_list_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Remove text within curly braces
    text = re.sub(r"\{.*?\}", "", text)

    # Filter out non-alphabetic characters and convert to lowercase
    filtered_text = re.sub(r"[^a-zA-Z\s]+", ' ', text)

    # Extract words from the filtered text
    words = re.findall(r"\b[a-zA-Z']+\b", filtered_text)

    # Filter out words with an apostrophe
    words = [word for word in words if "'" not in word]

    # Filter out words starting with uppercase letters
    words = [word for word in words if not word[0].isupper()]

    with open(word_list_file, 'r', encoding='utf-8') as file:
        word_list = file.read().lower().splitlines()

    s = ''
    unknown_words = set()
    for word in words:
        result = lemma.word_stem(word.lower())
        if result is not None:
            if text_file.lower().endswith('.srt') or text_file.lower().endswith('.txt'):
                if len(word) > 3 and str(result[0]) not in word_list:
                    if len(str(result[0])) == 3 and str(result[0]).endswith('s'):
                        continue
                    unknown_words.add(word)
                    s += str(result[0]) + ' '

    # Remove duplicate stems
    unknown_words = remove_duplicates(s)
    return unknown_words

# Specify the text folder and choose the first file in the folder
text_folder = 'raw_word'
text_file = os.listdir(text_folder)[0]

# Specify the word list file
word_list_file = "word_list.txt"

# Find unknown words in the text file
unknown_words = find_unknown_words(os.path.join(text_folder, text_file), word_list_file)

# Print each unknown word and the total count
for i in unknown_words.split():
    print(i)
print(len(unknown_words.split()))
