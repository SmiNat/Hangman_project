''' Projekt na zaliczenie
    Plik @github:
        - projekt: https://github.com/SmiNat/Hangman_project/blob/main/Hangman_project.py
        - treść zadania: https://github.com/SmiNat/Hangman_project/blob/main/zadanie_zaliczeniowe.md
        - cytaty: (pobrano z: https://github.com/JamesFT/Database-Quotes-JSON/blob/master/quotes.json)
        - hasła z podpowiedziami: (pobrano z: https://github.com/le717/PHP-Hangman/tree/master/words)
        - hasła bez podpowiedzi: (pobrano z: https://github.com/hevalhazalkurt/HangmanPy/blob/master/words.txt)
'''
import json
import random
import re

# Basic tools (variables, definitions):
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


def hidden_guess(quote: str, used_characters: list[str]=[]):
    '''Changes characters in string into low line ("_").
       Special characters like -,.' are not changed.
       Space sign is replaced by double space for better eye-view'''
    final_quote = quote.replace(",","").replace(".","")
    hidden_quote = []
    for character in final_quote:
        if character.lower() in used_characters:
            sign = character.lower()+" "
            hidden_quote.append(sign)
        elif character == " ":
            sign = "  "
            hidden_quote.append(sign)
        elif character in ["-", "'"]:
            sign = character
            hidden_quote.append(sign)
        else:
            sign = "_"+" "
            hidden_quote.append(sign)
    hidden_quote = ",".join(hidden_quote).replace(",","")
    return hidden_quote

def characteristics(quote: str):
    '''Shows basic game characteristics of a randomly selected word/quote'''
    special_characters = []
    characters = []
    space_sign = 0
    for char in quote.lower():
        if char in ["-", "'", ",", "."]:
            if char not in special_characters:
                special_characters.append(char)
        elif char == " ":
            space_sign+=1
        else:
            if char not in characters:
                characters.append(char)
    characters.sort()
    print("\nNumber of overall characters: {}\n"
          "Number of unique characters: {}, including:\n"
          "\t- ordinary characters [alphabet letters]: {}\n"
          "\t- special characters {}: {}\n"
          "Space signs: {}".format(len(quote), len(characters)+len(special_characters), len(characters), special_characters, len(special_characters), space_sign))
    return characters
    # print("Characters to guess:", characters)                     # DO UKRYCIA / USUNIĘCIA!


hangman = (
            """
            ------
            |    |
            |
            |
            |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |
            |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |   -+-
            |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |  /-+
            |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |  /-+-\\
            |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |  /-+-\\
            |    |
            |
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |  /-+-\\
            |    |
            |   /
            |
            ----------
            """,
            """
            ------
            |    |
            |    O
            |  /-+-\\
            |    |
            |   / \\
            |
            ----------
            """)

# External data for words/quotes:
# Source: https://github.com/SmiNat/Hangman_project

file_path_quotes = r"quotes_from_JamesFT.json"              # from (and with great appreciation to) https://github.com/JamesFT/Database-Quotes-JSON/blob/master/quotes.json
file_path_words = r"words_from_hevalhazalkurt.txt"          # from (and with great appreciation to) https://github.com/hevalhazalkurt/HangmanPy/blob/master/words.txt
file_path_words_with_hints = r"word-list_from_le717.json"   # from (and with great appreciation to) https://github.com/le717/PHP-Hangman/blob/master/words/word-list.json

files = {1:file_path_words_with_hints, 2:file_path_words, 3:file_path_quotes}
to_guess = ""               # searched word/quote
max_number_of_attempts = 7  # maximum number of attempts per game
no_attempts = 0             # number of attempts used by the player
attempt = ""                # letter/word/quote chosen by the player
used_letters = []           # letters used by the player

# ---THE GAME---
# Introduction
intro = '''----- INTRODUCTION -----
The goal of this game is to guess hidden word or quote. 
The word/quote to guess is represented by a row of dashes representing each letter of the word (only alphabet letters are hidden). 
You reveal dashes by choosing a letter from alphabet. If the letter occurs in word/quote it is revealed in all its correct positions. 
If the suggested letter does not occur in the word, you loose one of attempts to guess the word/quote and one element of a hanged stick figure is drawn as a tally mark.
You may, at any time, attempt to guess the whole word/quote. If the word is correct, you win the game. Otherwise, you loose one of attempts to guess the word/quote and another element is added to the hangmen diagram. 
If all of the of attempts to guess the word/quote are used -  the diagram  of a hangman is complete and the game is lost. 
If you reveal all the letters that appear in the word/quote before the diagram is completed - you win the game.
------------------------'''

# Choosing a game level
print(intro+"\n")
print('''Level of difficulty:
      1 - low difficulty - word with hint
      2 - medium difficulty - word without hint
      3 - high difficulty - quote (Author revealed)
      ''')

difficulty_level = input("Choose level of difficulty (type number from 1 to 3): ")

# Selecting a word/quote to guess:
while True:
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
        else:
            assert difficulty_level in [1,2,3], "Chosen number out of range!"
    except AssertionError as e:
        print("--- Error:\n--- Invalid choice - difficulty level must be expressed as a number between 1 and 3.")
        print(f"--- Error code: {e} ---")
        difficulty_level = input("Choose difficulty level (type number from 1 to 3): ")
    except FileNotFoundError as e:
        print("--- Error:\n--- External file with quotes is missing. Download file {} from https://github.com/SmiNat/Hangman_project".format(files[int(difficulty_level)]))
        print(f"--- Error code: {e} ---")
        difficulty_level = input("Choose difficulty level (type number from 1 to 3): ")
    except ValueError as e:
        print("--- Error:\n--- Invalid choice - the choice must be expressed as a digit.")
        print(f"--- Error code: {e} Number: {difficulty_level} ---")              # do zastanowienia czemu nie działa wywołanie Number: {}
        difficulty_level = input("Choose difficulty level (type number from 1 to 3): ")
    except Exception as e:
        print(f"--- Error:\n--- {e} ---")
        difficulty_level = input("Choose difficulty level (type number from 1 to 3): ")
    else:
        print("\n"+"-"*30+"\n")
        print(f"Number of guesses: {max_number_of_attempts}")
        print("Level of difficulty:", end=" ")
        print("high") if difficulty_level == 3 else print("medium") if difficulty_level == 2 else print("low")
        print("Category:", end=" ")
        print("quotes") if difficulty_level == 3 else print("words")
        characters = characteristics(to_guess)
        print("\n" + "-" * 30 + "\n")
        print(hangman[0])
        print("To guess: ", end=" ")
        print(hidden_guess(to_guess))
        print("Author: {}".format(author)) if difficulty_level == 3 else print("Hint: {}".format(hint)) if difficulty_level == 1 else print("Hint: none")
        break

print(to_guess)                              # DO UKRYCIA / USUNIĘCIA!
print(characters)
# Choosing a letter or guessing a word/quote:
while attempt.replace(" ","") != to_guess.lower().replace(" ","") and no_attempts<max_number_of_attempts:
    attempt = input("Choose a letter or enter the whole word/quote: ").lower()
    if attempt.replace(" ","") == to_guess.lower().replace(" ",""):
        break
    elif len(attempt)>1:
        print("You can only choose one letter at a time or you can try to guess the whole word/quote by typing an answer (the length of the answer must be equal to the length of hidden word/quote).")
    else:
        if attempt.isalpha():
            if attempt in used_letters:
                print("You have already tried this letter. Choose different letter.")
            else:
                used_letters.append(attempt)
                if all(item in used_letters for item in characters):
                    break
                elif attempt in to_guess.lower():
                    print("The letter '{}' occurs {} {} in the search word/quote".format(attempt, to_guess.lower().count(attempt), "time" if to_guess.lower().count(attempt)==1 else "times"))
                else:
                    no_attempts += 1
                    print("No letter '{}' found".format(attempt))
                print(hangman[no_attempts])
                print(hidden_guess(to_guess, used_letters))
                print("Attempts used: {}/{}. Letters used: {}".format(no_attempts,max_number_of_attempts, used_letters))
        else:
            print("Use only alphabet letters.")
if no_attempts == max_number_of_attempts:
    print(hangman[no_attempts])
    print("GAME OVER! You have been hanged!")
else:
    print("Congratulations! You have found a correct answer!")

