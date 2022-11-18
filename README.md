# MPCPy

Exemple d'un reproductor MP3 amb Python basat amb MPD i MPC per GNU Linux.

## Requeriments

- GNU Linux: Ubuntu 22.04.1 LTS
- python >= 3.8
- MPD: Music Player Daemon 0.23.5 (0.23.5)
- MPC: A minimalist command line interface to MPD

## MPD
https://www.musicpd.org/
https://mpd.readthedocs.io/en/stable/user.html

- apt install mpd
- configure /etc/mpd.conf
```
music_directory "/home/aleon/Música"
playlist_directory "/home/aleon/playlists"
auto_update "yes"
...
```
- load mp3 music in music_directory
- sudo systemctl enable mpd
- sudo systemctl start mpd
- sudo systemctl status mpd
- reboot if is necessary

## MPC
https://www.musicpd.org/clients/mpc/
https://www.musicpd.org/doc/mpc/html/

- apt install mpc
- mpc update
- mpc ls
- mpd add /
- mpc play

## mpcpy_aleon

- DIR_MUSIC = '/home/aleon/Música' (= /etc/mpd.conf)
- DIR_PLAYLIST = '/home/aleon/playlists' (/etc/mpd.conf)

## files

- **albums**: albums objects pickel
- **estat_reproductor**: MPC current state
- **playlist.txt**: current playlist
- **playlists.txt**: list of playlist
- **info.txt**: album information in album folder
```
gender
year
author
```

## Run

- python3 mpcpy_aleon.py
