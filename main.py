import tkinter as tk
from PIL import Image, ImageTk
# List of words for Hangman
from PIL.Image import Resampling
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
        self.invalid_guess = None
        self.game_over = None
        self.showinfo_congrats = None
        self.winner_image = None
        self.logo_label = None
        self.showinfo_already_guessed = None
        self.master = master
        self.master.title('Hangman Game')
        self.word = ''
        self.word_to_guess = ''
        self.guesses_left = 6
        self.guessed_letters = []
        self.master.geometry('700x500')
        # Prevent window resizing
        self.master.resizable(False, False)
        self.score = 0

        # Logo Image
        self.logo_image = []
        image = Image.open('logo.png')
        image = image.resize((100, 50), Resampling.LANCZOS)
        logo_image = ImageTk.PhotoImage(image)
        self.logo_image.append(logo_image)

        # Load hangman images
        self.hangman_images = []
        for i in range(8):
            image = Image.open(f'src\hangman_{i}.png')  # Replace with your image filenames
            image = image.resize((250, 250), Resampling.LANCZOS)
            hangman_image = ImageTk.PhotoImage(image)
            self.hangman_images.append(hangman_image)

        # Create GUI components
        self.word_label = tk.Label(self.master, text='', font=('Helvetica', 24))
        self.word_label.pack(pady=10)

        # Create leaderboard button
        self.leaderboard_button = tk.Button(self.master, text='Leaderboard', font=('Helvetica', 10),
                                            command=self.leaderboard_command)
        self.leaderboard_button.place(x=550, y=86)

        self.showinfo_alreadyguessed = tk.Label(self.master, text='Guess a letter:', font=('Helvetica', 14))
        self.showinfo_alreadyguessed.pack()

        self.guess_entry = tk.Entry(self.master, font=('Helvetica', 14), justify='center')
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.master, text='Guess', font=('Helvetica', 14), command=self.check_guess)
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(self.master, text='New Game', font=('Helvetica', 14), command=self.new_game)
        self.reset_button.pack(pady=10)

        self.hint_button = tk.Button(self.master, text='Hint', font=('Helvetica', 10), command=self.hint_button)
        self.hint_button.place(x=500, y=87)

        self.score_label = tk.Label(self.master, text=f'Score: {self.score}', font=('Helvetica', 10, 'bold'))
        self.score_label.place(x=105, y=130)

        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.pack()

        self.new_game()

    def new_game(self):
        self.logo_label = tk.Label(self.master, image=self.logo_image[0])
        self.logo_label.place(x=90, y=75)
        self.word = get_random_word()

        # Testing word
        print(self.word)

        self.word_to_guess = '_' * len(self.word)
        self.guesses_left = 7
        self.guessed_letters = []
        # self.word_label.config(text=self.word_to_guess)
        self.word_label.config(text=' '.join(self.word_to_guess))
        self.draw_hangman(0)
        self.hint_button.config(state='normal')  # Enable the hint button

    def leaderboard_command(self):
        pass

    def hint_button(self):
        # Get a random letter from the word that hasn't been guessed yet
        hint_letter = ''
        for letter in self.word:
            if letter not in self.guessed_letters:
                hint_letter = letter
                break
        # Update the word to guess with the hint letter
        self.update_word_to_guess(hint_letter)
        # Decrement the number of guesses left
        self.guesses_left -= 1
        self.draw_hangman(6 - self.guesses_left)
        # Disable the hint button after it has been used
        self.hint_button.config(state='disabled')

    def check_guess(self):
        guess = self.guess_entry.get()
        self.guess_entry.delete(0, 'end')
        if guess.isalpha() and len(guess) == 1:
            if guess in self.guessed_letters:
                self.showinfo_already_guessed = tk.Label(self.master,
                                                         text=f'You have already guessed the letter "{guess}".')
                self.showinfo_already_guessed.place(x=415, y=130)
                self.showinfo_already_guessed.config(fg='red', font=('Comic Sans MS', 10, 'bold'))
                self.master.after(1500, self.showinfo_already_guessed.destroy)  # Destroy the label after 1.5 seconds
            elif guess in self.word:
                self.guessed_letters.append(guess)
                self.update_word_to_guess(guess)
                if '_' not in self.word_to_guess:
                    self.showinfo_congrats = tk.Label(self.master,
                                                      text=f'Congratulations, You guessed the word "{self.word}" correctly!.')
                    self.showinfo_congrats.place(x=90, y=450)
                    self.showinfo_congrats.config(fg='green', font=('Comic Sans MS', 14, 'bold'))
                    self.master.after(4000, self.showinfo_congrats.destroy)
                    self.new_game()
                else:
                    self.score += 10  # Increment score by 10 for correct letter guess
                    self.score_label.config(text=f'Score: {self.score}')  # Update score label
            else:
                self.guessed_letters.append(guess)
                self.guesses_left -= 1
                self.draw_hangman(6 - self.guesses_left)
                if self.guesses_left == -1:
                    self.game_over = tk.Label(self.master, text=f'The word was "{self.word}".')
                    self.game_over.place(x=210, y=450)
                    self.game_over.config(fg='red', font=('Comic Sans MS', 14, 'bold'))
                    self.score = 0
                    self.master.after(4000, self.game_over.destroy)
                    self.new_game()
        else:
            self.invalid_guess = tk.Label(self.master, text='Please enter a valid single letter guess.')
            self.invalid_guess.place(x=245, y=93)
            self.master.after(1000, self.invalid_guess.destroy)

    def update_word_to_guess(self, letter):
        new_word_to_guess = ''
        for i in range(len(self.word)):
            if self.word[i] == letter:
                new_word_to_guess += letter
                self.score += 10
            else:
                new_word_to_guess += self.word_to_guess[i]
        self.word_to_guess = new_word_to_guess
        self.word_label.config(text=' '.join(self.word_to_guess))

    def draw_hangman(self, guesses):
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor='nw', image=self.hangman_images[guesses])


if __name__ == '__main__':
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()
