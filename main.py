import json
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
        # Create leaderboard window
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title('Leaderboard')
        leaderboard_window.geometry('300x300')

        # Load leaderboard data from json file
        leaderboard_data = self.load_leaderboard_data()

        # Sort leaderboard data by score in descending order
        leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

        # Display top 3 names and scores in leaderboard window
        top_3_names = []
        top_3_scores = []
        for i in range(min(3, len(leaderboard_data))):
            top_3_names.append(leaderboard_data[i]['name'])
            top_3_scores.append(leaderboard_data[i]['score'])

        for i in range(len(top_3_names)):
            label = tk.Label(leaderboard_window, text=f"{i + 1}. {top_3_names[i]}: {top_3_scores[i]}",
                             font=('Helvetica', 14))
            label.pack(pady=5)

        # Close button
        close_button = tk.Button(leaderboard_window, text='Close', font=('Helvetica', 14),
                                 command=lambda: leaderboard_window.destroy())
        close_button.pack(pady=30)

    def update_leaderboard(self, name, score):
        # Load leaderboard data from json file
        leaderboard_data = self.load_leaderboard_data()

        # Add player name and score to leaderboard data
        leaderboard_data.append({'name': name, 'score': score})

        # Sort leaderboard data by score in descending order
        leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

        # Save updated leaderboard data to json file
        self.save_leaderboard_data(leaderboard_data[:10])  # Keep only top 10 scores

        # Save name and score msg display

    def load_leaderboard_data(self):
        # Load leaderboard data from json file
        try:
            with open('leaderboard.json', 'r') as f:
                leaderboard_data = json.load(f)
        except FileNotFoundError:
            # If json file not found, initialize with an empty list
            leaderboard_data = []
        return leaderboard_data

    def update_leaderboard_prompt_name(self, score):
        if self.guesses_left == -1:
            # Create a new Toplevel window for entering name
            name_window = tk.Toplevel(self.master)
            name_window.title('Enter Your Name')
            name_window.geometry('300x200')

            # Label and Entry for entering name
            name_label = tk.Label(name_window, text='Enter Your Name:', font=('Helvetica', 14))
            name_label.pack(pady=5)

            name_entry = tk.Entry(name_window, font=('Helvetica', 14))
            name_entry.pack(pady=5)

            # Label for displaying saved message
            saved_label = tk.Label(name_window, text='', font=('Helvetica', 14))
            saved_label.pack(pady=5)

            # Function to update leaderboard and show saved message
            def update_leaderboard_and_show_saved_message():
                name = name_entry.get()
                self.update_leaderboard(name, score)
                saved_label.config(text='Name and score have been saved.')

            # Button for submitting name
            submit_button = tk.Button(name_window, text='Submit', font=('Helvetica', 14),
                                      command=update_leaderboard_and_show_saved_message)
            submit_button.pack(pady=5)

            # Close button
            close_button = tk.Button(name_window, text='Close', font=('Helvetica', 14),
                                      command=lambda: name_window.destroy())
            close_button.pack(pady=5)
        else:
            self.update_leaderboard('', score)

    def save_leaderboard_data(self, leaderboard_data):
        # Save leaderboard data to json file
        with open('leaderboard.json', 'w') as f:
            json.dump(leaderboard_data, f)

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
                    self.update_leaderboard_prompt_name(self.score)
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
