import tkinter as tk
# List of words for Hangman
import requests


def get_random_word():
    # Call the random word API and get a random word
    response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
    if response.status_code == 200:
        word = response.json()[0]
        return word
    else:
        raise Exception('Failed to get random word from API')


# Hangman game class
class HangmanGame:
    def __init__(self, master):
      self.none = None
