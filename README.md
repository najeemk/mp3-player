# MP3 Player
A simple, small, terminal based MP3 music player built in Python 3.
## Installation <br>
<strong>Note: All commands issued here are for Unix. I have yet to test this package on Windows. </strong><br><br>
First install VLC media player. Next, clone this repository and go to the repository folder. I am using a virtual environment for the packages in this repository; I suggest you do the same. To make a virtual environment, input: <br> `python3 -m virtualenv env`<br><br> in the source folder. Now, to activate this virtual environment, input: <br> `source env/bin/activate`<br><br>
Next, you will need to install the VLC and Mutagen packages on pip: <br>
`pip install vlc %% pip install mutagen` <br>
Make sure to create a /songs folder, if not already existing, on the same directory as the player.py file.
## Usage <br>
To run the program, simply type `python3 player.py`. The program will by default pool songs from a /songs folder, however, a user specified file can be passed to the program instead.
<br><br>Note: I am not responsible if anything happens to your files while using this product. There is no liability or warranty whatsovever.
