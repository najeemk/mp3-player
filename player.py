""" VLC based MP3 music player
"""
import os
import time
import vlc
import sys
from mutagen.mp3 import MP3
from random import randint

vlc_song = None
shuffle = False

def scan_directory(directory):
    """ Returns a list of the songs inside inputted folder.

    Args: 
        directory (str): string of the songs directory
    Returns: 
        list: list of songs in the directory
    """

    def given_dir():
        for filename in os.listdir(directory):
            if (filename.lower().find(".mp3") != - 1):
                song_file_names.append(filename)
        if len(song_file_names) < 1:
            print("Please add songs to /songs and reload the program")
            quit()
        
    if directory == "":
        print("Using Default Directory (/songs)")
        directory = str(os.getcwd() + "/songs")
    else:
        directory = directory.strip()

    song_file_names = []
    print("Scanning: " + directory + "\n")

    try:
        given_dir()
        song_file_names.sort()
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
    global shuffle
    if shuffle == True:
        return randint(0, len(song_list_dir) - 1)
    print("\nWhich song should I play? ")
    song_number = (input("If nothing is selected, a random song will play: "))
    print("")
    if (song_number.lower() == "exit"):
        print("Goodbye...\n")
        time.sleep(1)
        quit()
    elif (song_number.lower() == "shuffle"):
        shuffle = True
        return randint(0, len(song_list_dir) - 1)
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

    def song_dur():
        print("Starting")
        start_time = time.time()
        time.sleep(0.5)
        while ((time.time() - start_time) < song_duration):
            os.system('cls' if os.name == 'nt' else 'clear')
            dur_str = "| Song Duration: " + ( \
                seconds_to_hms(time.time() - start_time) + "/" + \
                 seconds_to_hms(song_duration))
            print(" " + ("-" * (dash_len - 1)))
            # Prints the now playing section
            print("| Now playing: " + song_name, end="")
            print(" " * abs((dash_len) - len(song_name) - \
            len_of_song_duration_str + 1) + "|" )
            # Prints the song duration section
            print(dur_str, end="")
            print(" " * abs(dash_len - len(dur_str)) + "|")
            # Prints the exit command
            print(exit_str, end="")
            print(" " * abs((dash_len) - len(exit_str)) + "|" )
            #Prints the bottom border
            print(" " + ("-" * (dash_len - 1)))
            time.sleep(1)

    song_duration = mut_song.info.length
    len_of_song_duration_str = 16
    exit_str = "| >To stop the song, close the terminal or hit 'ctrl + c'"
    dash_len = max(len(exit_str) + 1, len(song_name) + len_of_song_duration_str)
    song_dur()

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
    
    if shuffle == True:
        which_song = song_picker()
    else:
        print("Enter song number you wish to play, or exit to quit program:\n")
        for counter, e in enumerate(song_list_dir):
            print(str(counter + 1) + ": " + str(e))
        print("shuffle: Shuffle songs")
        print("exit: Exit program")
        which_song = song_picker()
    vlc_song, mut_song, song_name = current_song(which_song)
    vlc_song.play()
    # During debug mode, song_duration flag does is not enabled
    song_info(mut_song, song_name)
    vlc_song.stop()
    print("\nSong Finished!\n")
    print("-" * 60)


print("\nMP3 MUSIC PLAYER (DEBUGGING MODE)")
print("=" * 60)
song_dir = input("Enter songs directory here (defaults to /songs): ")
song_list_dir, song_dir = scan_directory(song_dir)
exit_command = ""
while True:
    song_init()
    time.sleep(1)