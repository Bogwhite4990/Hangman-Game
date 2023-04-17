# Hangman Game

This is a simple Hangman game implemented in Python using the tkinter library for the graphical user interface (GUI) and the PIL library for image processing.

## Getting Started

To run the Hangman game, you need to have Python 3 installed on your system. You also need to install the required libraries - tkinter and PIL.

You can install the required libraries using the following commands:

pip install tk
pip install pillow

Once you have installed the required libraries, you can simply copy the provided code and save it in a Python file with a .py extension. Then you can run the Python file using any Python interpreter.

python hangman_game.py

## Game Rules

1. The game randomly selects a word from a word API and displays the word as underscores to represent the hidden letters.
2. The player can guess a letter by typing it in the guess entry field and clicking the "Guess" button.
3. If the guessed letter is correct and is present in the word, the game reveals the letter in the word.
4. If the guessed letter is incorrect, the game draws a part of the hangman figure.
5. The player has 7 chances to guess the word correctly before the hangman figure is complete and the game is over.
6. The player can also use the "Hint" button to get a hint letter from the word, but it will decrement the number of guesses left.
7. If the player correctly guesses the word within the allowed number of guesses, they win the game. Otherwise, they lose.

## GUI Components

word_label: Label to display the word to be guessed.
leaderboard_button: Button to display the leaderboard (currently not implemented).
guess_entry: Entry field to input the guessed letter.
guess_button: Button to submit the guessed letter.
reset_button: Button to start a new game.
hint_button: Button to get a hint letter.
score_label: Label to display the current score.
canvas: Canvas to draw the hangman figure.

## Class Description

HangmanGame: Class that represents the Hangman game. It has methods to initialize the game, start a new game, handle guessed letters, update the word to guess, draw the hangman figure, and manage game state.

## Screenshots
![image](https://user-images.githubusercontent.com/103454208/232488192-22082f08-f364-44f1-9e27-1d92fdb78aec.png)


## Contributing
If you would like to contribute to this Hangman game project, you can fork the repository, make changes, and create a pull request. You can also report issues or suggest enhancements through the Issues tab.
