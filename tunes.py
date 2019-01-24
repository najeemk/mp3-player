""" VLC based music player
"""
import os
import time
import vlc
from mutagen.mp3 import MP3
from random import randint

def scan_directory(directory):
    """ Returns a list of the songs inside inputted folder.

    Args: 
        directory (str): string of the songs directory
    Returns: 
        list: list of songs in the directory
    """

    def given_dir():
        for filename in os.listdir(directory):
            song_file_names.append(filename)
        
    if directory == "":
        directory = str(os.getcwd() + "/songs")
    else:
        directory = directory.strip()

    song_file_names = []
    print("Scanning: " + directory + "\n")

    try:
        given_dir()
        return song_file_names, directory
    except FileNotFoundError:
        print("Not a valid directory! \nUsing default directory instead\n")
        directory = str(os.getcwd() + "/songs")
        given_dir()
        return song_file_names, directory


def song_picker():
    """ Allows user to select song, from index 1, making sure that input 
    is valid.

    Returns:
        int: number of song selected

    """
    print("\nWhich song should I play? ")
    song_number = (input("If nothing is selected, a random song will play: "))
    print(song_number)
    if (song_number.lower() == "exit"):
        print("Goodbye...")
        time.sleep(3)
        quit()
    try:
        song_number = int(song_number)
        song_number = song_number - 1
        while (song_number + 1 > len(song_list_dir)):
            print("Please pick a valid number!")
            song_number = int(input("\nWhich song should I play: ")) - 1
        return song_number
    except ValueError:
        return randint(0, len(song_list_dir) - 1)


def song_path(song_index):
    """ Given a directory, a list of songs, and the particular index of a song
    the method will return both a normal song path and the VLC specific
    song path.

    Args:
        song_index (int): song selected by the user
    Returns: 
        str: file path of song
        MediaPlayer: returns intialized VLC media player with song
    """
    song_directory = song_dir + "/" + song_list_dir[song_index]
    song_vlc_directory = vlc.MediaPlayer("file://" + song_directory)

    return song_directory, song_vlc_directory

def current_song(song):
    """ Initializes both VLC and Mutagen to play/read from the selected song.

    Args:
        song (int): song selected by the user
    Returns:
        MediaPlayer: returns intialized VLC media player with song
        MP3: mutagen mp3 file
        str: name of the song
        
    """
    current_song_directory = song_list_dir
    mut_dir, vlc_song = song_path(song)
    song_name = current_song_directory[song]
    mut_song = MP3(mut_dir)

    return vlc_song, mut_song, song_name

def song_info(mut_song, song_name):
    """ Prints song info and returns song duration

    Args:
        mut_song (MP3): mutagen mp3 file
        song_name (str): name of the song
    Returns:
        str: song duration in hours, minutes, and seconds
    """

    song_duration = mut_song.info.length
    exit_str = "| >To stop the song, close the terminal or hit 'ctrl + c'"
    dur_str = "| Song Duration: " + seconds_to_hms(song_duration)
    # len_of_song_duration_str measures the length of "| Song Duration: " - 1
    len_of_song_duration_str = 16
    dash_len = max(len(exit_str) + 1, len(song_name) + len_of_song_duration_str)

    # The code below draws a box around the now playing sign
    print(" " + ("-" * dash_len) +"\n| Now playing: " + song_name, end="")
    print(" " * abs((dash_len) - len(song_name) - len_of_song_duration_str + 1) + "|" )
    print(exit_str, end="")
    print(" " * abs((dash_len) - len(exit_str)) + "|" )
    print(dur_str, end="")
    print(" " * abs(dash_len - len(dur_str)) + "|")
    print(" " + ("-" * dash_len))

    return song_duration

def seconds_to_hms(seconds):
    """ Converts time from seconds to a more human readable hours, 
    minutes, and seconds

    Args: 
        seconds (int, float): time in seconds
    Returns: 
        str: time in hours, minutes, and seconds
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return ("%d:%02d:%02d" % (h, m, s))

def song_init():
    """ Initalizes new song selection.
    """
    for counter, e in enumerate(song_list_dir):
        print(str(counter + 1) + ": " + str(e))
    print("exit: Exit program")
    which_song = song_picker()
    vlc_song, mut_song, song_name = current_song(which_song)
    vlc_song.play()
    duration = song_info(mut_song, song_name)
    time.sleep(10)
    vlc_song.stop()
    print("\nSong Finished!\n")


print("\nSong Picker")
print("-" * 60)
song_dir = input("Enter songs directory here: ")
song_list_dir, song_dir = scan_directory(song_dir)
exit_command = ""
while True:
    song_init()
    time.sleep(3)
os.system('cls' if os.name == 'nt' else 'clear')