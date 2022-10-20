#!/usr/bin/env python3
from typing import Final
import time
start_time = time.time()

filestub = '/Users/mattparker/Dropbox/python/five_letter_words/'

def load_words():
    words_txt = f'{filestub}words_alpha.txt'
    with open(words_txt) as word_file:
        valid_words = word_file.read().split()
    return valid_words

word_length = 5

word_length2 = word_length*2
word_length4 = word_length2*2
word_length5 = word_length4 + word_length

# number of scanA increases per progress report
stepgap = 1000

# Yes, that is the alphabet. In the default order python makes a list in. Weird.
alphabet = ['f', 'g', 'o', 'q', 't', 'b', 'y', 'h', 'r', 'u', 'j', 'w', 'i', 'p', 's', 'd', 'l', 'e', 'k', 'm', 'n', 'v', 'z', 'c', 'a', 'x']

# I could be clever and write this to be dynamic
# but for now I'll hard code everything assuming five words
number_of_sets = 5

english_words = load_words()

print(f"{len(english_words)} words in total")

fl_words = [w for w in english_words if len(w) == word_length]

print(f"{len(fl_words)} words have {word_length} letters")


word_sets = []

unique_fl_words = []
for w in fl_words:
    unique_letters = set(w)
    if len(unique_letters) == word_length:
        if unique_letters not in word_sets:
            word_sets.append(unique_letters)
            unique_fl_words.append(w)

number_of_words = len(unique_fl_words)

print(f"{number_of_words} words have a unique set of {word_length} letters")

doubleword_sets = []
doubleword_words = []

scanA = 0
while scanA + 1 < number_of_words:
    scanB = scanA + 1
    while scanB < number_of_words:
        give_it_a_try = word_sets[scanA] | word_sets[scanB]
        if len(give_it_a_try) == word_length2:
            doubleword_sets.append(give_it_a_try)
            doubleword_words.append([unique_fl_words[scanA], unique_fl_words[scanB]])
        scanB += 1
    scanA += 1

number_of_doublewords = len(doubleword_sets)

print(f"we found {number_of_doublewords} combos")

counter = 0

success_found = []

scanA = 0
print(f"starting at position {scanA}")

while scanA < number_of_doublewords-1:
    if scanA % stepgap == 0:
        print(f"Up to {scanA} after {time.time() - start_time} seconds.")

    scanB = scanA + 1
    while scanB < number_of_doublewords:
        give_it_a_try = doubleword_sets[scanA] | doubleword_sets[scanB]
        if len(give_it_a_try) == word_length4:
            scanC = 0
            while scanC < number_of_words:
                final_go = give_it_a_try | word_sets[scanC]
                if len(final_go) == word_length5:
                    success = doubleword_words[scanA] + doubleword_words[scanB]
                    success.append(unique_fl_words[scanC])
                    success.sort()
                    if success not in success_found:
                        success_found.append(success)
                        print(success)
                scanC += 1
            counter += 1
        scanB += 1
    scanA += 1

print(f"Damn, we had {len(success_found)} successful finds!")
print(f"That took {time.time() - start_time} seconds")

print("Here they all are:")
for i in success_found:
    print(i)

print("DONE")
