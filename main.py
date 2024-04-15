import customtkinter
import os
import random
import pygame
from tkinter import ttk
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

pygame.mixer.init()

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

current_note = None
previous_note = None
chances_remaining = 3

def play_note():
    global current_note
    if current_note is not None:
        note_file = f"{current_note}.wav"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        note_path = os.path.join(script_dir, "Keys", note_file)
        pygame.mixer.music.load(note_path)
        pygame.mixer.music.play()

def check_guess(note):
    global current_note, chances_remaining
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    if note == current_note:
        display_message("Correct!")
        chances_remaining = 3
        show_next_round_button()
    else:
        chances_remaining -= 1
        if chances_remaining == 0:
            display_message(f"Incorrect. The correct note is {current_note}.")
            chances_remaining = 3
            show_next_round_button()
            show_listen_right_note_button()
        else:
            display_message(f"Incorrect. {chances_remaining} chances remaining.")

def listen_to_note():
    global current_note
    play_note()

def listen_to_right_note():
    play_note()

def generate_new_note():
    global current_note, previous_note
    while True:
        current_note = random.choice(notes)
        if current_note != previous_note:
            previous_note = current_note
            break

def display_message(message):
    message_label.configure(text=message)

def show_next_round_button():
    next_round_button.grid(row=row_num + 3, column=0, columnspan=4, pady=10)
    listen_button.configure(text="Listen to Note")

def show_listen_right_note_button():
    listen_button.configure(text="Listen to Right Note")

def next_round():
    next_round_button.grid_forget()
    listen_right_note_button.grid_forget()
    generate_new_note()
    play_note()
    display_message("Guessing The Note!")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("LOOP")

listen_button = customtkinter.CTkButton(app, text="Listen to Note", command=listen_to_note)
listen_button.grid(row=0, column=0, columnspan=4, pady=10)

row_num = 1
col_num = 0

for note in notes:
    note_button = customtkinter.CTkButton(app, text=note, command=lambda n=note: check_guess(n),)
    note_button.grid(row=row_num, column=col_num, padx=10, pady=10)
    col_num += 1
    if col_num == 4:
        col_num = 0
        row_num += 1

message_label = customtkinter.CTkLabel(app, text="")
message_label.grid(row=row_num + 1, column=0, columnspan=4, pady=10)

next_round_button = customtkinter.CTkButton(app, text="Next Round", command=next_round)
next_round_button.grid(row=row_num + 3, column=0, columnspan=4, pady=10)
next_round_button.grid_forget()

listen_right_note_button = customtkinter.CTkButton(app, text="Listen to Right Note", command=listen_to_right_note)
listen_right_note_button.grid(row=row_num + 3, column=0, columnspan=4, pady=10)
listen_right_note_button.grid_forget()

for i in range(4):
    app.grid_columnconfigure(i, weight=1)

app.grid_rowconfigure(row_num + 2, weight=1)

generate_new_note()
display_message("Guessing The Note!")

app.mainloop()
