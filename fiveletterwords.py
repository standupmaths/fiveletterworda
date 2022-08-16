import functools
import string

# Read all words
with open("words_alpha.txt") as f:
    words = [word.strip() for word in f]

print(f"Total words: {len(words):,}")

# Keep only words with length 5
words_len5 = [word for word in words if len(word) == 5]

print(f"Words with length 5: {len(words_len5):,}")

# Remove words with repeating alphabets
words_len5_dedup = [word for word in words_len5 if len(set(word)) == 5]

print(f"Words with length 5 without repeating alphabets: {len(words_len5_dedup):,}")

# Remove anagrams
words_len5_alpha_set = set()
words_len5_filtered = set()
for word in words_len5_dedup:
    alphabets = str(sorted(word))
    if alphabets not in words_len5_alpha_set:
        words_len5_alpha_set.add(alphabets)
        words_len5_filtered.add(word)

print(
    f"Words with length 5 without repeating alphabets or anagrams: {len(words_len5_filtered):,}"
)

# Create a dict of alphabet -> words that contain this alphabet
alphabet_words = {alphabet: set() for alphabet in string.ascii_lowercase}

for word in words_len5_filtered:
    for alphabet in word:
        alphabet_words[alphabet].add(word)

# Get list of alphabets in increasing order of frequency
alphabets_sorted = []
for k, v in alphabet_words.items():
    alphabets_sorted.append((len(v), k))
alphabets_sorted.sort()

for count, alphabet in alphabets_sorted:
    print(alphabet, f"{count:,}")


# Function to find combinations
#   - alphabets: alphabets not used till now
#   - words: valid words using the above alphabets
@functools.lru_cache(maxsize=1024)
def find_combos(alphabets, words):
    if not words or not alphabets:
        return []
    if len(alphabets) == 5:
        # 5 alphabets left, there can be at max 1 word since we've removed anagrams
        return [[word] for word in words]

    ret = []
    # Consider the least frequent alphabet that we've not used till now
    for count, alphabet in alphabets_sorted:
        if alphabet in alphabets:
            # Consider all words containing this alphabet which are in the `words` set
            for word in alphabet_words[alphabet]:
                if word in words:
                    # Create a set without any words which contains alphabets in the current word
                    rem = words
                    for alphabet in word:
                        rem -= alphabet_words[alphabet]

                    # Recursion!
                    ret += [
                        [word] + rest
                        for rest in find_combos(frozenset(alphabets - set(word)), rem)
                    ]
            break

    return ret


combos = []
total = 0
for alphabet in string.ascii_lowercase:
    ret = find_combos(
        frozenset(set(string.ascii_lowercase) - {alphabet}),
        frozenset(words_len5_filtered - alphabet_words[alphabet]),
    )
    combos += ret
    total += len(ret)
    print(f"Number of combos without {alphabet}: {len(ret):,}")
print(f"Total combos: {total:,}")
print("\nCombos:")
for combo in combos:
    print(combo)
