from tkinter import Menu, Tk, Listbox, Frame, Button, PhotoImage, Scale, Label, HORIZONTAL, END
import pygame
import os
from mutagen.mp3 import MP3
import time

# Initialize the root window
root = Tk()
root.title("myMusicPlayer")
root.geometry("600x400")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False

# Labels for the time display
time_label = Label(root, text="00:00 / 00:00")
time_label.grid(row=2, column=1)

# Create a Scale widget for the progress bar
progress_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=500)
progress_bar.grid(row=3, column=0, columnspan=4)

def load_music():
    global current_song
    root.directory = "C:/Users/Administrator/Desktop/fajjer/music"

    # Clear previous song list
    songs.clear()
    songlist.delete(0, END)

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext.lower() == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    if songs:  # Ensure there's at least one song in the list
        songlist.selection_set(0)
        current_song = songs[songlist.curselection()[0]]
        update_time_label()  # Update time label when the song loads

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Load Music from fajjer/music', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

# Create the Listbox
songlist = Listbox(root, bg="purple4", fg="white", width=100, height=15)
songlist.grid(row=0, column=0, columnspan=4)

# Load button images
nextbuttonimage = PhotoImage(file='next.png')
backbuttonimage = PhotoImage(file='previous.png')
playbuttonimage = PhotoImage(file='play.png')
pausebuttonimage = PhotoImage(file='pause.png')

# Create a control frame
control_frame = Frame(root)
control_frame.grid(row=1, column=0, columnspan=4, pady=10)

# Add buttons to the control frame
next_button = Button(control_frame, image=nextbuttonimage, borderwidth=0, command=lambda: next_music())
next_button.grid(row=0, column=3, padx=7, pady=10)

back_button = Button(control_frame, image=backbuttonimage, borderwidth=0, command=lambda: back_music())
back_button.grid(row=0, column=0, padx=7, pady=10)

play_button = Button(control_frame, image=playbuttonimage, borderwidth=0, command=lambda: play_music())
play_button.grid(row=0, column=1, padx=7, pady=10)

pause_button = Button(control_frame, image=pausebuttonimage, borderwidth=0, command=lambda: pause_music())
pause_button.grid(row=0, column=2, padx=7, pady=10)

# Event handling functions
def play_music():
    global current_song, paused
    try:
        if not paused:
            pygame.mixer.music.load(os.path.join(root.directory, current_song))
            pygame.mixer.music.play()
            update_progress_bar()  # Start updating the progress bar
        else:
            pygame.mixer.music.unpause()
            paused = False
    except Exception as e:
        print(f"Error playing music: {e}")

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except IndexError:
        print("No more songs in the list")

def back_music():
    global current_song, paused
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except IndexError:
        print("No previous songs in the list")

def update_progress_bar():
    # Get the length of the current song
    song_path = os.path.join(root.directory, current_song)
    song_mut = MP3(song_path)
    song_length = song_mut.info.length

    # Update the progress bar based on the elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
    progress_bar.config(to=song_length)  # Set the maximum value of the progress bar to the song length
    progress_bar.set(current_time)

    # Update the time label
    elapsed_time = time.strftime("%M:%S", time.gmtime(current_time))
    total_time = time.strftime("%M:%S", time.gmtime(song_length))
    time_label.config(text=f"{elapsed_time} / {total_time}")

    # Schedule the function to run again after 1000 milliseconds (1 second)
    if pygame.mixer.music.get_busy():
        root.after(1000, update_progress_bar)

def update_time_label():
    # Update the time label when a new song is selected
    song_path = os.path.join(root.directory, current_song)
    song_mut = MP3(song_path)
    song_length = song_mut.info.length
    total_time = time.strftime("%M:%S", time.gmtime(song_length))
    time_label.config(text=f"00:00 / {total_time}")

# Start the Tkinter event loop
root.mainloop()
