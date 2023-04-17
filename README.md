# Hangman Game

This is a simple implementation of the classic game Hangman in Python.

## How to Play

1. Run the Python script `hangman.py` on your local machine.
2. The game will select a random word from the list of words provided.
3. Guess the letters one by one by typing them in the terminal.
4. If the guessed letter is correct, it will be revealed in the word.
5. If the guessed letter is incorrect, a part of the hangman figure will be drawn.
6. Keep guessing letters until you correctly guess the entire word or run out of attempts.
7. You can customize the number of attempts allowed or the list of words in the script.

## How to Run

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the directory where the `hangman.py` script is located.
3. Run the script using the Python interpreter: `python hangman.py`
4. Follow the instructions displayed in the terminal to play the game.

## Customization

You can customize the following variables in the `hangman.py` script:

- `words`: List of words to be used in the game. You can add or remove words as desired.
- `max_attempts`: Maximum number of attempts allowed for guessing a letter. You can change this value to increase or decrease the difficulty of the game.

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
