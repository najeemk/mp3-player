""" VLC based music player
"""
import os
import time
import vlc
from mutagen.mp3 import MP3

def scan_directory(directory):
    """ Returns a list of the songs inside inputted folder.

    Args: 
        directory (str): string of the songs directory
    Returns: 
        list: list of songs in the directory

    """
    song_file_names = []

    for filename in os.listdir(directory):
        song_file_names.append(filename)

    return song_file_names

def song_path(directory, song_list, song_index):
    """ Given a directory, a list of songs, and the particular index of a song
    the method will return both a normal song path and the VLC specific
    song path.

    Args:
        directory (str): string of the songs directory
        song_list (list): list of songs
        song_index (int): song selected by the user
    Returns: 
        str: file path of song
        MediaPlayer: returns intialized VLC media player with song

    """
    song_directory = directory + "/" + song_list[song_index]
    song_vlc_directory = vlc.MediaPlayer("file://" + song_directory)

    return song_directory, song_vlc_directory

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

def current_song(files_directory, song):
    """ Initializes both VLC and Mutagen to play/read from the selected song.

    Args:
        files_directory (str): directory of the song files
        song (int): song selected by the user
    Returns:
        MediaPlayer: returns intialized VLC media player with song
        MP3: mutagen mp3 file
        str: name of the song
        
    """
    current_song_directory = scan_directory(files_directory)
    mut_dir, vlc_song = song_path(files_directory, current_song_directory, song)
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

    print("\nNow playing: " + song_name)
    print(">To stop the song, close the terminal or hit 'ctrl + c'")
    song_duration = mut_song.info.length
    print("Song Duration: " + seconds_to_hms(song_duration) + "\n")

    return song_duration

def song_picker(files_directory):
    """ Allows user to select song, from index 1, making sure that input 
    is valid.

    Args:
        files_directory (str):  string of the songs directory
    Returns:
        int: number of song selected

    """
    song_number = int(input("\nWhich song should I play: ")) - 1
    while (song_number + 1 > len(scan_directory(files_directory))):
        print("Please pick a valid number!")
        song_number = int(input("\nWhich song should I play: ")) - 1

    return song_number

def song_init():
    """ Initalizes new song selection.
    """
    files_directory = input("Enter songs directory here: ")
    for counter, e in enumerate(scan_directory(files_directory)):
        print(str(counter + 1) + ": " + str(e))
    which_song = song_picker(files_directory)
    vlc_song, mut_song, song_name = current_song(files_directory, which_song)
    vlc_song.play()
    duration = song_info(mut_song, song_name)
    time.sleep(duration)
    print("Song Finished!\n")

print("\nSong Picker")
print("-" * 60)
song_init()
time.sleep(3)
os.system('cls' if os.name == 'nt' else 'clear')