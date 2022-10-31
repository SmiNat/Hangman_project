''' Projekt na zaliczenie
    Plik @github:
        - projekt: https://github.com/SmiNat/Hangman_project/blob/main/Hangman_project.py
        - treść zadania: https://github.com/SmiNat/Hangman_project/blob/main/zadanie_zaliczeniowe.md
        - cytaty: (pobrano z: https://github.com/JamesFT/Database-Quotes-JSON/blob/master/quotes.json)
        - hasła z podpowiedziami: (pobrano z: https://github.com/le717/PHP-Hangman/tree/master/words)
        - hasła bez podpowiedzi: (pobrano z: https://github.com/hevalhazalkurt/HangmanPy/blob/master/words.txt)
'''
import json
import os
import random
import re

# quote = ""

def random_quote_from_file(file_path: str):
    '''Returns random quote from designated JSON file.
        Quotes with special characters (like ;:%@ etc.) and digits are excluded.'''
    with open(file_path, "r") as file:
        quotes_database = json.load(file)
    match = True
    while match:
        random_guess = random.choice(quotes_database)
        pattern = re.compile(r"[^- ',.a-zA-Z_]")
        match = pattern.search(random_guess["quoteText"])
    return random_guess

def random_word_without_hint_from_file(file_path: str):
    '''Returns random word without hint from designated .txt file.
        Words with less than 6 characters are excluded.'''
    with open(file_path, "r") as file:
        quotes_database = file.read().splitlines()
        while True:
            random_guess = random.choice(quotes_database)
            if len(random_guess)>5:
                break
    return random_guess

def random_word_with_hint_from_file(file_path: str):
    '''Returns random word with hint from designated JSON file.'''
    with open(file_path, "r") as file:
        quotes_database = json.load(file)
        random_guess = random.choice(quotes_database)
    return random_guess


def hidden_guess(quote: str):
    '''Changes characters in string into low line ("_").
       Special characters like -,.' are not changed.
       Space sign is replaced by double space for better eye-view'''
    for character in quote:
        if character == " ":
            sign = "  "
        elif character in ["-", "'", ",", "."]:
            sign = character
        else:
            sign = "\u0332 "+" "
        print(sign, end="")

def characteristics(quote: str):
    special_characters = []
    characters = []
    space = 0
    for char in quote.lower():
        if char in ["-", "'", ",", "."]:
            if char not in special_characters:
                special_characters.append(char)
        elif char == " ":
            space+=1
        else:
            if char not in characters:
                characters.append(char)
    characters.sort()
    print("\nNumber of overall characters: {}\n"
          "Number of unique characters: {}, including:\n"
          "\t- ordinary characters [alphabet letters]: {}\n"
          "\t- special characters {}: {}\n"
          "Space signs: {}".format(len(quote), len(characters)+len(special_characters), len(characters), special_characters, len(special_characters), space))
    print("Characters to guess:", characters)                     # DO UKRYCIA / USUNIĘCIA!


file_path_quotes = r"quotes_from_JamesFT.json"
file_path_words = r"words_from_hevalhazalkurt.txt"
file_path_words_with_hints = r"word-list_from_le717.json"

files = {1:file_path_words_with_hints, 2:file_path_words, 3:file_path_quotes}



'''Guess a quote'''
intro = '''The goal of this game is to quess hidden word or quote. 
The word/quote to guess is represented by a row of dashes representing each letter of the word (only alphabet letters are hidden). 
You reveal dashes by choosing a letter from alphabet. If the letter occurs in word/quote it is revealed in all its correct positions. 
If the suggested letter does not occur in the word, you loose one of attempts to guess the word/quote and one element of a hanged stick figure is drawn as a tally mark.
You may, at any time, attempt to guess the whole word. If the word is correct, you win the game. Otherwise, you loose one of attempts to guess the word/quote and another element is added to the hangmen diagram. 
If all of the of attempts to guess the word/quote are used -  the diagram  of a hangman is complete and the game is lost. 
If you reveal all the letters that appear in the word/quote before the diagram is completed - you win the game.'''

print(intro+"\n")
print('''Level of difficulty:
      1 - low difficulty - word with hint
      2 - medium difficulty - word without hint
      3 - high difficulty - quote (Author revealed)
      ''')

difficulty_level = input("Choose difficulty level (number from 1 to 3): ")

try:
    difficulty_level = int(difficulty_level)
    if difficulty_level == 3:
        quote = random_quote_from_file(files[3])
        to_guess = quote["quoteText"]
        author = quote["quoteAuthor"]
    elif difficulty_level == 2:
        word = random_word_without_hint_from_file(files[2])
        to_guess = word
    elif difficulty_level == 1:
        word = random_word_with_hint_from_file(files[1])
        to_guess = word["word"]
        hint = word["hint"]
except FileNotFoundError as e:
    print("External file with quotes is missing."
          "Download file {} from https://github.com/SmiNat/Hangman_project".format(files[int(difficulty_level)]))
    print("--- Error specifics: {} ---".format(e))
except Exception as e:
    print("---Error! Specifics: {} ---".format(e))


print("-"*10, "\nLevel of difficulty:", end=" ")
print("high") if difficulty_level == 3 else print("medium") if difficulty_level == 2 else print("low")
print("Category:", end=" ")
print("quotes") if difficulty_level == 3 else print("words")
print("Author: {}".format(author)) if difficulty_level == 3 else print("Hint: {}".format(hint)) if difficulty_level == 1 else print("Hint: none")
print("To guess: ")
to_quess_hidden = hidden_guess(to_guess)
characteristics(to_guess)

