from typing import *
from collections import defaultdict
import random 
import functools

cache = functools.lru_cache(None)

Word  = str # A word is a lower-case string of five different letters
Reply = str # A reply is five characters taken from 'GY.': Green, Yellow, Miss
Green, Yellow, Miss = 'GY.'

words = open('wordle-small.txt').read().upper().split() #  2,315 target words
words_big = open('wordle-big.txt').read().upper().split()

target = "HELLO"                   #test target for debug
#target = random.choice(words)       #random target word from wordle-small.txt

Letter = list()    #list of letters to check against


@cache
def reply_for(guess, target) -> Reply: 
    "The five-character reply for this guess on this target in Wordle."
    # We'll start by having each reply be either Green or Miss ...
    reply = [Green if guess[i] == target[i] else Miss for i in range(5)]
    # ... then we'll change the replies that should be yellow
    counts = Counter(target[i] for i in range(5) if guess[i] != target[i])
    for i in range(5):
        if reply[i] == Miss and counts[guess[i]] > 0:
            counts[guess[i]] -= 1
            reply[i] = Yellow
    return ''.join(reply)

@cache
def reply_letters(guess, target) -> Letter:
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    guess_split = list(guess)
    target_split = list(target)

    green_letters = [target[i] for i in range(5) if guess[i] == target[i]]
    yellow_letters = [guess[i] for i in range(5) if guess_split[i] in target_split and guess_split[i] != target_split[i]]
    miss_letters = [guess[i] for i in range(5) if guess_split[i] not in target_split]
    
    remaining_letters = [alphabet[i] for i in range(26) if alphabet[i] not in guess_split]

    return green_letters, yellow_letters, miss_letters, remaining_letters


def main():
    guesses_left = 6                    #6 guesses

    guessed_words = []                  #No repeats

    green_letters = []
    yellow_letters = []
    miss_letters = []
    remaining_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


    while guesses_left > 0:
        unclean_input = input("Please type your five-letter guess: ")
        
        #Omit words not == len(5)
        if len(unclean_input) != 5:
            print("Incorrect word input size, please try again. ")
            continue
        
        #Make input uppercase
        clean_input = unclean_input.upper()

        #Check if valid 5 letter word in big wordlist
        if clean_input not in words_big:
            print("Invalid word. Please try again")
            continue
        
        #Check input against repeats
        if clean_input in guessed_words:
            print("Repeat entry, try again.")
            continue
        else:
            guessed_words.append(clean_input)
        
        #Get Green, Yellow, Miss reply_for
        response = reply_for(clean_input, target)
        print("{} : {}".format(clean_input, response))

        
        #Adjust letters reamining
        rep_letters = reply_letters(clean_input, target)

        for item in rep_letters[0]:
            if item in green_letters:
                pass
            else:
                green_letters.extend(item)
        
        for item in rep_letters[1]:
            if item in yellow_letters:
                pass
            else:
                yellow_letters.extend(item)
        
        for item in rep_letters[2]:
            if item in miss_letters:
                pass
            else:
                miss_letters.extend(item)

        for item in remaining_letters:
            if item in rep_letters[3]:
                pass
            else:
                remaining_letters.remove(item)

        #remaining_letters_ret = list(set(remaining_letters + rep_letters[3]))
        print("Green Letters: {} \nYellow Letters: {} \nWrong Letters: {} \nRemaining Letters: {}".format(green_letters, yellow_letters, miss_letters, remaining_letters))
        
        #Adjust guesses left
        guesses_left -= 1
        print("Guesses left: {}".format(guesses_left))

        #Winner case
        if response == 'GGGGG':
            print("Congrats! You win. The word this time was: {}".format(target))
            break
        
    #Loser case when no guesses left       
    if guesses_left == 0 and response != 'GGGGG':
        print("You ran out of guesses before solving, better luck next time")
        print("The word this time was: {}".format(target))



if __name__ == '__main__':
    main()