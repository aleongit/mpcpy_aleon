# MPCPy

Exemple d'un reproductor MP3 amb Python basat amb MPD i MPC per consola GNU Linux.
Ús de classes, gestió de llistes de reproducció, fitxers i metadades ID3.

## Requeriments

- GNU Linux (Arch, Ubuntu)
- python >= 3.8
- MPD: Music Player Daemon 0.23.5 (0.23.5)
- MPC: A minimalist command line interface to MPD / mpc version: 0.34
- eyeD3: Python tool for working with audio files, specifically MP3 files containing ID3 metadata

## MPD
https://www.musicpd.org/
https://mpd.readthedocs.io/en/stable/user.html

- sudo pacman -S mpd (**arch**)
- apt install mpd (**ubuntu**)
- configure /etc/mpd.conf
- add permissions rx for others (user mpd) in all of necessary folders
- add permissions rx for others in /home/user if is necessary
```
music_directory "/home/aleon/Música"
playlist_directory "/home/aleon/playlists"
user "mpd"
auto_update "yes"
audio_output {
        type            "alsa"
        name            "My ALSA Device"
#       device          "hw:0,0"        # optional
#       mixer_type      "hardware"      # optional
#       mixer_device    "default"       # optional
##      mixer_control   "PCM"           # optional
##      mixer_index     "0"             # optional
}
#
...
```
- load mp3 music in music_directory
- add info.txt in every album directory with gender, year and author 
- sudo systemctl enable mpd
- sudo systemctl start mpd
- sudo systemctl status mpd
- check errors, files, directories and folder permissions
- reboot if is necessary

## MPC
https://www.musicpd.org/clients/mpc/
https://www.musicpd.org/doc/mpc/html/

- sudo pacman -S mpc (**arch**)
- apt install mpc (**ubuntu**)
- mpc update
- mpc ls
- mpd add /
- mpc play

## mpcpy_aleon

- DIR_MUSIC = '/home/aleon/Music' (= /etc/mpd.conf)
- DIR_PLAYLIST = '/home/aleon/playlists' (/etc/mpd.conf)

## files

- **albums**: album objects pickel
- **estat_reproductor**: MPC current state
- **playlist.txt**: current playlist
- **playlists.txt**: list of playlist
- **info.txt**: album information in album folder
```
gender
year
author
```

## eyeD3
https://eyed3.readthedocs.io/en/latest/
https://eyed3.readthedocs.io/en/latest/eyed3.id3.html#module-eyed3.id3.tag

- sudo pacman -S python-pip
- pip install eyeD3


## Run

- python mpcpy_aleon.py

- main
```
INTRO    Play/Pause
>           Següent (next)
<          Anterior (prev)
+[N]        + Volum
-[N]        - Volum
r     Random on/off 
A            Àlbums (album objects = album folders)
L     Load Playlist (load playlist to listen to)
C    Crear Playlist (generate playlist from album objects by criteria)
R             Reset (init and clear)
0            Sortir (exit)
```

- create playlist
```
Crear llista Reproducció
------------------------
1 -> Gènere (gender)
2 -> Autor (author)
3 -> Anys (years)
4 -> Reproduccions (reproductions)
5 -> Paraula (word)
6 -> Àlbum (album)
0 -> <<
```

- albums
```
Sants Sistema
Gènere: Reggae
Any: 2006
Autor: Pirat's Sound Sistema
Reproduccions: 0
Ruta: /home/aleon/Music/Pirat's Sound Sistema/Sants Sistema
Cançons: 13
Borrades: []

Editar Àlbum
------------------------
E -> Editar àlbum
I -> Info MP3
- -> Eliminar cançons
+ -> Afegir cançons eliminades
0 -> <<
```

- info mp3
```
/home/aleon/Music/Pirat's Sound Sistema/Sants Sistema/1-11 A Cada Somni.mp3
# =============================================================================
Track Name:     A Cada Somni
Track Artist:   Pirat's Sound Sistema
Track Album:    Sants Sistema
Track Duration: 0:00:04:59
Track Number:   CountAndTotalTuple(count=11, total=None)
Track BitRate:  (False, 128)
Track BitRate:  128 kb/s
Sample Rate:    44100
Mode:           Stereo
# =============================================================================
Album Artist:         Pirat's Sound Sistema
Album Year:           2006
Album Recording Date: 2006
Album Type:           None
Disc Num:             CountAndTotalTuple(count=1, total=None)
Artist Origin:        None
# =============================================================================
Artist URL:         None
Audio File URL:     None
Audio Source URL:   None
Commercial URL:     None
Copyright URL:      None
Internet Radio URL: None
Publisher URL:      None
Payment URL:        None
# =============================================================================
Publisher: PROPAGANDA PEL FET!
Original Release Date: None
Play Count: None
Tagging Date: None
Release Date: None
Terms Of Use: None
isV1: False
isV2: True
BPM: 92
Cd Id: None
Composer: None
Encoding date: None
# =============================================================================
Genre: Reggae
Non Std Genre Name: Reggae
Genre ID: 16
Non Std Genre ID: 16
LAME Tag:       {}
# =============================================================================
```