'''
Practice script for playing hangman locally using the Trexsim practice 
dictionary of 250,000 words. Note: the real game must be played through the
Trexsim API and uses a separate dictionary consisting of 250,000 disjoint 
entries.
'''

import re
import collections
import random

# Load the 250,000-word dictionary
def load_dictionary(dictionary_file):
    with open(dictionary_file, "r") as file:
        return file.read().splitlines()

# Pair-based frequency analysis to determine the next guess
def guess_next_letter(current_pattern, guessed_letters, current_dictionary):
    # Convert the current pattern (e.g., "_ p p _ e") to a regex-friendly string
    clean_word = current_pattern.replace("_", ".")
    len_word = len(clean_word)

    # Filter dictionary words based on the current pattern
    possible_words = []
    for word in current_dictionary:
        if len(word) == len_word and re.match(clean_word, word):
            possible_words.append(word)

    # If there are no matching words, default to original frequency analysis
    if not possible_words:
        possible_words = current_dictionary

    # Analyze letter pairs (bigrams) and their frequency in the possible words
    bigram_frequencies = collections.Counter()
    for word in possible_words:
        for i in range(len_word - 1):
            bigram = word[i:i + 2]
            if bigram[0] not in guessed_letters and bigram[1] not in guessed_letters:
                bigram_frequencies[bigram] += 1

    # If bigram frequency analysis doesn't suggest any new letters, fall back to single-letter frequency
    if bigram_frequencies:
        for bigram, _ in bigram_frequencies.most_common():
            if bigram[0] not in guessed_letters:
                return bigram[0]
            elif bigram[1] not in guessed_letters:
                return bigram[1]

    # Fallback to single-letter frequency analysis if bigrams don't help
    print('using single letter freq')
    single_letter_frequencies = collections.Counter("".join(possible_words))
    for letter, _ in single_letter_frequencies.most_common():
        if letter not in guessed_letters:
            return letter

    return None  # Shouldn't happen if the dictionary is correctly filtered

# Play a single game of Hangman using the local dictionary and guessing strategy
def play_hangman(word, dictionary):
    guessed_letters = []
    current_pattern = "_" * len(word)
    current_dictionary = dictionary.copy()

    tries_remaining = 6  # Standard number of guesses allowed
    while tries_remaining > 0 and "_" in current_pattern:
        guess = guess_next_letter(current_pattern, guessed_letters, current_dictionary)
        guessed_letters.append(guess)

        if guess in word:
            # Update the pattern to reflect the newly guessed letter
            current_pattern = "".join([letter if letter in guessed_letters else "_" for letter in word])
            print(f"Correct guess: {guess}. Current word: {current_pattern}")
        else:
            tries_remaining -= 1
            print(f"Incorrect guess: {guess}. Tries remaining: {tries_remaining}")

    if "_" not in current_pattern:
        print(f"Congratulations! You guessed the word: {word}")
        return True
    else:
        print(f"Out of tries! The word was: {word}")
        return False

# Main function to load the dictionary and test the game
def main():
    # Load the local 250,000-word dictionary
    dictionary = load_dictionary("words_250000_train.txt")
    
    # Test word for the hangman game (you can replace this with any word)
    N = 50
    num_correct = 0
    for k in range(N):
        test_word = random.choice(dictionary)
    
        # Play the hangman game using the test word
        res = play_hangman(test_word, dictionary)
        if res: num_correct += 1
            
    print(f"Final result: {num_correct/N} accuracy")

if __name__ == "__main__":
    main()