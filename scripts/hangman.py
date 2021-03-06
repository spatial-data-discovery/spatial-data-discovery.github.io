# This script runs a simple hangman game in command line. 
#
# Last edit: 2/10/20

#required modules
import random
import argparse

class Hangman(object):
    # Opens up the dictionary
    def __init__(self, level = 5, non_ascii = False, dictionary = 'american'):
        self.file_object = open(dictionary, 'r').read().split()
        self.non_ascii = non_ascii
        self.level = level
        return

    def play(self):
        # Letter that can be present in a word
        normal_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'"]
        normal_checker = 0
        # Chooses an eligible word from the dictionary
        first_word = random.choice(self.file_object).lower()
        if len(first_word) < self.level:
            first_word = random.choice(self.file_object).lower()
        if self.non_ascii == False:
            while normal_checker == 0:
                for i in first_word:
                    if i not in normal_letters:
                        first_word = random.choice(self.file_object).lower()
                        if len(first_word) < self.level:
                            first_word = random.choice(self.file_object).lower()
                    elif (i in normal_letters) and (i is first_word[len(first_word) - 1]):
                        normal_checker = 1
                    else:
                        pass
        # Removes apostrophe(s) from the word
        if "'" in first_word:
            first_word = list(first_word)
            first_word.remove("'")
            first_word = ''.join(first_word)
            print('Word contains an apostrophe. Apostrophe has been removed.')
        word = ' '.join(first_word)
        x = ' ' * len(word)
        incorrect_count = 0
        g = 0
        letters_guessed = ''

        # Multiple board states for different stages of the game
        boards = [
        '-----\n|   |\n' + '|\n' * 6,

        '-----\n|   |\n' + '|   O\n' + '|\n' * 5,

        '-----\n|   |\n' + '|   O\n' + '|   |\n' + '|\n' * 4,

        '-----\n|   |\n' + '|   O\n' + '|  /|\n' + '|\n' * 4,

        '-----\n|   |\n' + '|   O\n' + '|  /|\\\n' + '|\n' * 4,

        '-----\n|   |\n' + '|   O\n' + '|  /|\\\n' '|  /\n' + '|\n' * 3,

        '-----\n|   |\n' + '|   O\n' + '|  /|\\\n' '|  / \\\n' + '|\n' * 3
        ]

        print(boards[0] + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters:')
        # Handles guessing procedure for the game
        while (x not in word) and (g == 0):
            same_letter = 0
            long_letter = 0
            duplicate_guess = 0
            letter = input('Guess a letter:  ')
            if (letter in x) or (letter in letters_guessed):
                duplicate_guess = 1
            print('\n')
            if duplicate_guess == 0:
                for i in range(0, len(word)):
                        if letter is word[i]:
                            x = list(x)
                            x[i] = letter
                            x = ''.join(x)
                            if same_letter == 0:
                                print('Correct!')
                            same_letter = 1
                        elif len(letter) > 1:
                            long_letter = 1
                        elif i == len(word) - 1 and same_letter == 0:
                            incorrect_count += 1
                            if incorrect_count == 6:
                                print('Incorrect.')
                                g = 1
                            else:
                                print('Incorrect. Guess again.')
                            letters_guessed += ' ' + letter
                        else:
                            pass
            # Handles error if more than one character is guessed
            if long_letter == 1:
                print(boards[incorrect_count] + x + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters: ' + letters_guessed + '\n' + '\nPlease only enter one letter.')
            # Handles error if a letter that has been guessed is guessed again
            elif duplicate_guess == 1:
                print(boards[incorrect_count] + x + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters: ' + letters_guessed + '\n' + '\nYou already guessed this letter.')
            elif (x not in word) and (g == 0) and (duplicate_guess == 0):
                print(boards[incorrect_count] + x + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters: ' + letters_guessed)

        if g == 1:
            print(boards[incorrect_count] + x + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters: ' + letters_guessed + '\n')
            print('\nYou lose! The word was ' + first_word + '.\n')

        if x in word:
            print(boards[incorrect_count] + x + '\n' + '- ' * len(first_word) + '\n' + 'Guessed Letters: ' + letters_guessed + '\n')
            print('You win!\n')

        play_again = input('Play again?(Y/N)  ')
        if (play_again == 'Y') or (play_again == 'y'):
            self.play()
        else:
            exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play hangman. All letters are lowercase and there are no symbols.')
    args = parser.parse_args()
    from hangman import *
    h = Hangman()
    h.play()