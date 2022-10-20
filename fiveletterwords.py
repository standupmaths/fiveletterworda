#!/usr/bin/env python3
from typing import Final
from time import time


def load_words():
    '''
    reads hardcoded word-file from storage into memory,
    parsing it as a `list` of words.
    '''
    filestub = '/Users/mattparker/Dropbox/python/five_letter_words/'
    words_txt = f'{filestub}words_alpha.txt'
    with open(words_txt, encoding='UTF-8') as word_file:
        valid_words = word_file.read().split()
    return valid_words

# global mutables are a nightmare!
WORD_LEN: Final = 5

WORD_LEN2: Final = WORD_LEN * 2
WORD_LEN4: Final = WORD_LEN2 * 2
WORD_LEN5: Final = WORD_LEN4 + WORD_LEN

STEP_GAP: Final = 1000
'''number of `scanA` increases per progress report'''
# for some reason, that doc-comment only works if the var is global

def main():
    '''this is where the program actually begins (after the header/definitions)'''
    # so it's fair to measure time from here
    # "see what I did there? a doc-comment that continues as a regular comment!" @Rudxain
    start_time: Final = time()

    english_words: Final = load_words()

    print(f"{len(english_words)} words in total")

    fl_words: Final = [w for w in english_words if len(w) == WORD_LEN]

    print(f"{len(fl_words)} words have {WORD_LEN} letters")


    word_sets: Final[list[set[str]]] = []
    unique_fl_words: Final[list[str]] = []

    for w in fl_words:
        unique_letters = set(w)
        if len(unique_letters) == WORD_LEN and unique_letters not in word_sets:
            word_sets.append(unique_letters)
            unique_fl_words.append(w)

    number_of_words: Final = len(unique_fl_words)

    print(f"{number_of_words} words have a unique set of {WORD_LEN} letters")

    doubleword_sets: Final[list[set[str]]] = []
    doubleword_words: Final[list[list[str]]] = []

    scanA = 0
    while scanA + 1 < number_of_words:
        scanB = scanA + 1
        while scanB < number_of_words:
            give_it_a_try = word_sets[scanA] | word_sets[scanB]
            if len(give_it_a_try) == WORD_LEN2:
                doubleword_sets.append(give_it_a_try)
                doubleword_words.append([unique_fl_words[scanA], unique_fl_words[scanB]])
            scanB += 1
        scanA += 1

    number_of_doublewords: Final = len(doubleword_sets)

    print(f"we found {number_of_doublewords} combos")

    success_found: Final[list[list[str]]] = []

    scanA = 0
    print(f"starting at position {scanA}")

    counter = 0
    while scanA < number_of_doublewords - 1:
        if scanA % STEP_GAP == 0:
            print(f"Up to {scanA} after {time() - start_time} seconds.")

        scanB = scanA + 1
        while scanB < number_of_doublewords:
            give_it_a_try = doubleword_sets[scanA] | doubleword_sets[scanB]
            if len(give_it_a_try) == WORD_LEN4:
                scanC = 0
                while scanC < number_of_words:
                    final_go = give_it_a_try | word_sets[scanC]
                    if len(final_go) == WORD_LEN5:
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

    # avoid measuring `print` latency
    end_time: Final = time() - start_time

    print(f"Damn, we had {len(success_found)} successful finds!")
    print(f"That took {end_time} seconds")

    print("Here they all are:")
    for i in success_found:
        print(i)

    print("-- DONE! --")

if __name__ == '__main__':
    main()